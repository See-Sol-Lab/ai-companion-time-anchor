"""Isolated Codex install/update/uninstall regression tests; no real user config is used."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install_hook.py"
SOURCE = ROOT / "hooks" / "user_prompt_submit.py"
WRAPPER = """
import importlib.util, sys
from pathlib import Path
from unittest.mock import patch
installer, home, *args = sys.argv[1:]
sys.argv = [installer, *args]
with patch('pathlib.Path.home', return_value=Path(home)):
    spec = importlib.util.spec_from_file_location('installer_under_test', installer)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
"""


class CodexInstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="time-anchor-installer-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "synthetic-home"
        self.home.mkdir()
        self.custom = self.base / "custom config with spaces"

    def run_installer(self, config: Path | str | None = None, *args: str) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        env.pop("CODEX_HOME", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        if config is not None:
            env["CODEX_HOME"] = str(config)
        return subprocess.run([sys.executable, "-c", WRAPPER, str(INSTALLER), str(self.home), *args],
            capture_output=True, text=True, env=env, timeout=30)

    def require_success(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stderr)

    def read_config(self, root: Path) -> dict:
        return json.loads((root / "hooks.json").read_text(encoding="utf-8"))

    def test_default_directory(self) -> None:
        self.require_success(self.run_installer())
        root = self.home / ".codex"
        self.assertEqual((root / "time-anchor/user_prompt_submit.py").read_bytes(), SOURCE.read_bytes())
        self.assertEqual(len(self.read_config(root)["hooks"]["UserPromptSubmit"]), 1)

    def test_custom_directory_reinstall_preserves_other_hooks_and_state(self) -> None:
        self.custom.mkdir()
        other = {"type": "command", "command": "python other-plugin.py", "timeout": 9}
        suffix = {"type": "command", "command": "python /tools/time-anchor/user_prompt_submit.py.backup"}
        old = {"type": "command", "command": "python '/old/custom root/time-anchor/user_prompt_submit.py'"}
        old_windows = {"type": "command", "commandWindows": 'python "C:\\previous config\\time-anchor\\user_prompt_submit.py"'}
        group = {"matcher": "*", "label": "preserve-group", "hooks": [old, other, suffix]}
        stop = [{"hooks": [{"type": "command", "command": "python stop.py"}]}]
        initial = {"description": "preserve-description", "unrelated": {"value": 7},
            "hooks": {"UserPromptSubmit": [group, {"hooks": [old_windows]}], "Stop": stop}}
        (self.custom / "hooks.json").write_text(json.dumps(initial), encoding="utf-8")
        snapshot = self.home / "Documents/Codex/.time-anchor/conversations/existing.json"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_bytes(b'{"version":2,"now_local":"2026-01-01T00:00:00+00:00"}')
        before = snapshot.read_bytes()

        self.require_success(self.run_installer(self.custom))
        installed = self.read_config(self.custom)
        self.assertEqual(installed["hooks"]["UserPromptSubmit"][0], {**group, "hooks": [other, suffix]})
        self.assertEqual(len(installed["hooks"]["UserPromptSubmit"]), 2)
        self.assertEqual(installed["hooks"]["Stop"], stop)
        self.assertEqual(installed["description"], initial["description"])
        self.assertEqual(installed["unrelated"], initial["unrelated"])
        handler = installed["hooks"]["UserPromptSubmit"][1]["hooks"][0]
        self.assertEqual(handler["additionalContextLimit"], 256)
        self.assertIn(str(self.custom / "time-anchor/user_prompt_submit.py"), handler["commandWindows"])
        self.assertFalse((self.home / ".codex").exists())
        self.assertEqual(snapshot.read_bytes(), before)
        first = (self.custom / "hooks.json").read_bytes()
        self.require_success(self.run_installer(self.custom))
        self.assertEqual((self.custom / "hooks.json").read_bytes(), first)
        self.assertEqual(snapshot.read_bytes(), before)
        self.assertEqual((self.custom / "time-anchor/user_prompt_submit.py").read_bytes(), SOURCE.read_bytes())

    def test_uninstall_preserves_state_and_unrelated_files(self) -> None:
        self.require_success(self.run_installer(self.custom))
        config = self.read_config(self.custom)
        other = {"hooks": [{"type": "command", "command": "python keep.py"}]}
        config["hooks"]["UserPromptSubmit"].append(other)
        (self.custom / "hooks.json").write_text(json.dumps(config), encoding="utf-8")
        note = self.custom / "time-anchor/keep.txt"
        note.write_bytes(b"keep")
        self.require_success(self.run_installer(self.custom, "--uninstall"))
        self.assertFalse((self.custom / "time-anchor/user_prompt_submit.py").exists())
        self.assertEqual(note.read_bytes(), b"keep")
        self.assertEqual(self.read_config(self.custom)["hooks"]["UserPromptSubmit"], [other])

    def test_invalid_config_does_not_replace_runtime(self) -> None:
        self.custom.mkdir()
        runtime = self.custom / "time-anchor/user_prompt_submit.py"
        runtime.parent.mkdir()
        runtime.write_bytes(b"existing runtime")
        for invalid in ["{", json.dumps({"hooks": {"UserPromptSubmit": "invalid"}})]:
            with self.subTest(config=invalid):
                (self.custom / "hooks.json").write_text(invalid, encoding="utf-8")
                self.assertNotEqual(self.run_installer(self.custom).returncode, 0)
                self.assertEqual(runtime.read_bytes(), b"existing runtime")
                self.assertEqual((self.custom / "hooks.json").read_text(encoding="utf-8"), invalid)

    def test_relative_codex_home_fails_clearly(self) -> None:
        result = self.run_installer("relative-config")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CODEX_HOME must be an absolute path", result.stderr)


if __name__ == "__main__":
    unittest.main()
