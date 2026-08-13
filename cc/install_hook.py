"""Install the Time Anchor UserPromptSubmit hook and skill into Claude Code.

This is the Claude Code port of the Codex installer. It targets the user-level
Claude configuration (~/.claude) so the time organ is available in ordinary
chat, and stays silent inside coding projects (see the hook's in_code_context).

    python install_hook.py              # install / update
    python install_hook.py --uninstall  # remove the hook (state is kept)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path


CLAUDE_DIR = Path.home() / ".claude"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
RUNTIME_DIR = CLAUDE_DIR / "time-anchor"
RUNTIME_SCRIPT = RUNTIME_DIR / "user_prompt_submit.py"
SKILLS_DIR = CLAUDE_DIR / "skills"

SOURCE_DIR = Path(__file__).resolve().parent
SOURCE_SCRIPT = SOURCE_DIR / "hooks" / "user_prompt_submit.py"
SOURCE_SKILL = SOURCE_DIR / "skills" / "time-anchor"

EVENT = "UserPromptSubmit"
# Stable substring used to recognise our own hook entry across installs.
MARKER = "/.claude/time-anchor/user_prompt_submit.py"


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


def read_settings() -> dict[str, object]:
    if not SETTINGS_FILE.exists():
        return {}
    value = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Invalid Claude settings file: {SETTINGS_FILE}")
    return value


def write_settings(settings: dict[str, object]) -> None:
    encoded = (json.dumps(settings, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    atomic_write(SETTINGS_FILE, encoded)


def is_time_anchor(handler: object) -> bool:
    if not isinstance(handler, dict):
        return False
    command = handler.get("command")
    return isinstance(command, str) and MARKER in command.replace("\\", "/").lower()


def strip_time_anchor(settings: dict[str, object]) -> None:
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return
    groups = hooks.get(EVENT)
    if not isinstance(groups, list):
        return
    remaining_groups: list[object] = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            remaining_groups.append(group)
            continue
        kept = [h for h in group["hooks"] if not is_time_anchor(h)]
        if kept:
            updated = dict(group)
            updated["hooks"] = kept
            remaining_groups.append(updated)
    if remaining_groups:
        hooks[EVENT] = remaining_groups
    else:
        hooks.pop(EVENT, None)
    if not hooks:
        settings.pop("hooks", None)


def hook_command() -> str:
    return f'"{sys.executable}" "{RUNTIME_SCRIPT}"'


def install() -> None:
    if not SOURCE_SCRIPT.is_file():
        raise FileNotFoundError(f"Missing Time Anchor hook source: {SOURCE_SCRIPT}")
    if not SOURCE_SKILL.is_dir():
        raise FileNotFoundError(f"Missing Time Anchor skill source: {SOURCE_SKILL}")

    # 1) Hook runtime.
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write(RUNTIME_SCRIPT, SOURCE_SCRIPT.read_bytes())

    # 2) Skill (so the active reader is callable in chat).
    skill_target = SKILLS_DIR / "time-anchor"
    if skill_target.exists():
        shutil.rmtree(skill_target)
    shutil.copytree(SOURCE_SKILL, skill_target)

    # 3) Register the hook in user settings, preserving everything else.
    settings = read_settings()
    strip_time_anchor(settings)
    handler = {"type": "command", "command": hook_command(), "timeout": 5}
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"Invalid 'hooks' section in {SETTINGS_FILE}")
    hooks.setdefault(EVENT, []).append({"hooks": [handler]})
    write_settings(settings)

    print(f"Installed Time Anchor hook runtime: {RUNTIME_SCRIPT}")
    print(f"Installed Time Anchor skill:        {skill_target}")
    print(f"Updated Claude user settings:       {SETTINGS_FILE}")
    print("Restart Claude Code so the new UserPromptSubmit hook is picked up.")
    print("Time Anchor stays silent inside git projects; set TIME_ANCHOR_FORCE=1 to override.")


def uninstall() -> None:
    if SETTINGS_FILE.exists():
        settings = read_settings()
        strip_time_anchor(settings)
        write_settings(settings)
    if RUNTIME_SCRIPT.exists():
        RUNTIME_SCRIPT.unlink()
    if RUNTIME_DIR.exists() and not any(RUNTIME_DIR.iterdir()):
        RUNTIME_DIR.rmdir()
    print("Removed the Time Anchor user hook. Skill and timestamp state were left intact.")
    print(f"To remove the skill too, delete: {SKILLS_DIR / 'time-anchor'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install the Time Anchor Claude Code user hook.")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    uninstall() if args.uninstall else install()


if __name__ == "__main__":
    main()
