from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


CODEX_DIR = Path.home() / ".codex"
HOOKS_FILE = CODEX_DIR / "hooks.json"
RUNTIME_DIR = CODEX_DIR / "time-anchor"
RUNTIME_SCRIPT = RUNTIME_DIR / "user_prompt_submit.py"
SOURCE_SCRIPT = Path(__file__).resolve().parent / "hooks" / "user_prompt_submit.py"
EVENT = "UserPromptSubmit"


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f"{path.name}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def read_config() -> dict[str, object]:
    if not HOOKS_FILE.exists():
        return {"description": "User lifecycle hooks.", "hooks": {}}
    value = json.loads(HOOKS_FILE.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("hooks"), dict):
        raise ValueError(f"Invalid Codex hooks file: {HOOKS_FILE}")
    return value


def is_time_anchor(handler: object) -> bool:
    if not isinstance(handler, dict):
        return False
    commands = (handler.get("command"), handler.get("commandWindows"))
    marker = "/.codex/time-anchor/user_prompt_submit.py"
    return any(
        isinstance(command, str)
        and marker in command.replace("\\", "/").lower()
        for command in commands
    )


def remove_time_anchor(config: dict[str, object]) -> None:
    hooks = config["hooks"]
    groups = hooks.get(EVENT, [])
    if not isinstance(groups, list):
        raise ValueError(f"Invalid {EVENT} hook list: {HOOKS_FILE}")

    remaining_groups: list[object] = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            remaining_groups.append(group)
            continue
        remaining_handlers = [
            handler for handler in group["hooks"] if not is_time_anchor(handler)
        ]
        if remaining_handlers:
            updated_group = dict(group)
            updated_group["hooks"] = remaining_handlers
            remaining_groups.append(updated_group)

    if remaining_groups:
        hooks[EVENT] = remaining_groups
    else:
        hooks.pop(EVENT, None)


def write_config(config: dict[str, object]) -> None:
    encoded = (json.dumps(config, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    atomic_write(HOOKS_FILE, encoded)


def install() -> None:
    if not SOURCE_SCRIPT.is_file():
        raise FileNotFoundError(f"Missing Time Anchor hook source: {SOURCE_SCRIPT}")

    atomic_write(RUNTIME_SCRIPT, SOURCE_SCRIPT.read_bytes())
    config = read_config()
    remove_time_anchor(config)
    handler = {
        "type": "command",
        "command": shlex.join([sys.executable, str(RUNTIME_SCRIPT)]),
        "commandWindows": subprocess.list2cmdline([sys.executable, str(RUNTIME_SCRIPT)]),
        "timeout": 3,
        "additionalContextLimit": 256,
    }
    config["hooks"].setdefault(EVENT, []).append({"hooks": [handler]})
    write_config(config)
    print(f"Installed Time Anchor hook runtime: {RUNTIME_SCRIPT}")
    print(f"Updated Codex user hooks: {HOOKS_FILE}")
    print("Restart Codex, open /hooks, and trust the Time Anchor UserPromptSubmit hook.")


def uninstall() -> None:
    if HOOKS_FILE.exists():
        config = read_config()
        remove_time_anchor(config)
        write_config(config)
    if RUNTIME_SCRIPT.exists():
        RUNTIME_SCRIPT.unlink()
    if RUNTIME_DIR.exists() and not any(RUNTIME_DIR.iterdir()):
        RUNTIME_DIR.rmdir()
    print("Removed the Time Anchor user hook. Timestamp state was left intact.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install the Time Anchor Codex user hook.")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    uninstall() if args.uninstall else install()


if __name__ == "__main__":
    main()
