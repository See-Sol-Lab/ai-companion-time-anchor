"""Regression tests for the Claude Code hook inside a coding project.

Inside a git project the hook must still record a snapshot every turn (so the
reader works there), stay silent on ordinary turns and incidental time words,
and speak only on a long gap / crossed date or a direct question about the time.
Outside a project it keeps the chat behaviour. TIME_ANCHOR_DISABLE=1 stays fully
silent and writes nothing.

Run: ``python tests/test_code_context.py``  (exit 0 = pass, 1 = failure)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "claude-code" / "hooks" / "user_prompt_submit.py"

WRAPPER = """
import importlib.util
import sys
from pathlib import Path

hook_path, state_dir = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("hook_under_test", hook_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.STATE_DIR = Path(state_dir)
module.main()
"""


def run(state_dir: Path, cwd: str, prompt: str, session: str, env_extra: dict[str, str] | None = None) -> str:
    env = dict(os.environ)
    env.pop("TIME_ANCHOR_FORCE", None)
    env.pop("TIME_ANCHOR_DISABLE", None)
    env.update(env_extra or {})
    event = {"hook_event_name": "UserPromptSubmit", "session_id": session, "prompt": prompt, "cwd": cwd}
    result = subprocess.run(
        [sys.executable, "-c", WRAPPER, str(HOOK), str(state_dir)],
        input=json.dumps(event).encode("utf-8"),
        capture_output=True,
        timeout=30,
        env=env,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8", "replace"))
    return result.stdout.decode("utf-8").strip()


def age_snapshot(state_dir: Path, hours: float) -> None:
    for path in state_dir.glob("*.json"):
        state = json.loads(path.read_text(encoding="utf-8"))
        earlier = datetime.fromisoformat(state["now_local"]) - timedelta(hours=hours)
        state["now_local"] = earlier.isoformat(timespec="seconds")
        path.write_text(json.dumps(state), encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        if not condition:
            failures.append(label)

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        (project / ".git").mkdir(parents=True)
        nested = project / "src"
        nested.mkdir()
        chat = Path(temp) / "chat"
        chat.mkdir()

        # Ordinary and incidental-time turns in a project: silent, but snapshot written.
        state = Path(temp) / "state-quiet"
        for _ in range(12):
            out = run(state, str(nested), "现在就需要检查这个了，大概要3天", "quiet")
            check("project: ordinary turn must stay silent", out == "")
        check("project: snapshot must still be written", len(list(state.glob("*.json"))) == 1)

        # Direct question in a project: attention cue.
        state = Path(temp) / "state-question"
        out = run(state, str(project), "现在几点了", "question")
        check("project: direct question must produce a cue", "attention cue" in out)
        out = run(state, str(project), "what time is it?", "question")
        check("project: English direct question must produce a cue", "attention cue" in out)

        # Long gap in a project: ambient context.
        state = Path(temp) / "state-gap"
        run(state, str(project), "fix the build", "gap")
        age_snapshot(state, 3)
        out = run(state, str(project), "ok continue", "gap")
        check("project: long gap must produce ambient context", "ambient context" in out)

        # Chat directory keeps the old behaviour: incidental time words get a cue.
        state = Path(temp) / "state-chat"
        out = run(state, str(chat), "今天有点累", "chat")
        check("chat: explicit time word must produce a cue", "attention cue" in out)

        # DISABLE: silent and no snapshot.
        state = Path(temp) / "state-disabled"
        out = run(state, str(chat), "现在几点了", "disabled", {"TIME_ANCHOR_DISABLE": "1"})
        check("disable: must stay silent", out == "")
        check("disable: must not write a snapshot", not state.exists() or not list(state.glob("*.json")))

    if failures:
        print("FAIL")
        for failure in failures:
            print(" -", failure)
        return 1
    print("PASS: code-context behaviour (silent, question, gap, chat, disable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
