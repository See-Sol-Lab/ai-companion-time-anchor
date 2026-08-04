from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path


STATE_DIR = Path.home() / "Documents" / "Codex" / ".time-anchor" / "conversations"


def state_path(session_id: str) -> Path:
    session_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    return STATE_DIR / f"{session_key}.json"


def utc_offset(value: datetime) -> str:
    total_minutes = int(value.utcoffset().total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def main() -> None:
    session_id = os.environ.get("CODEX_THREAD_ID")
    if not session_id:
        raise SystemExit(
            "Active Time Anchor requires a local Codex surface that exports CODEX_THREAD_ID."
        )

    path = state_path(session_id)
    if not path.exists():
        raise SystemExit(
            "Time Anchor hook snapshot for this conversation is unavailable. "
            "Install, review, and trust the Time Anchor user hook first."
        )

    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if snapshot.get("version") != 2 or not isinstance(snapshot.get("now_local"), str):
        raise SystemExit(f"Invalid Time Anchor hook snapshot: {path}")

    looked_at = datetime.now().astimezone()
    prompt_time = datetime.fromisoformat(snapshot["now_local"])
    payload = {
        "now_local": looked_at.isoformat(timespec="seconds"),
        "timezone": looked_at.tzname() or str(looked_at.tzinfo),
        "utc_offset": utc_offset(looked_at),
        "user_prompt_local": snapshot["now_local"],
        "previous_local": snapshot.get("previous_local"),
        "elapsed_seconds": snapshot.get("elapsed_seconds"),
        "elapsed_human": snapshot.get("elapsed_human"),
        "snapshot_age_seconds": round(max(0.0, (looked_at - prompt_time).total_seconds()), 3),
        "state_path": str(path),
        "source": "active read of the current conversation's hook snapshot",
    }
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
