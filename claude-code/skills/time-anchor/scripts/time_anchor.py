from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


# Displayed local timezone. Pinned to a fixed UTC+8 zone labeled "Taipei" so the
# surfaced timezone name never leaks a more specific region. Taipei observes no
# daylight saving, so a fixed offset stays correct year-round.
LOCAL_TZ = timezone(timedelta(hours=8), "Taipei")
BASE_DIR = Path.home() / "Documents" / "Claude" / ".time-anchor"
STATE_DIR = BASE_DIR / "conversations"
CORTEX_LOG = BASE_DIR / "temporal-cortex.jsonl"
TEMPORAL_CORTEX_CUE = (
    "Let this time check update your understanding of the moment. "
    "If the temporal facts change what this situation means, let that change naturally shape your response."
)


def session_key(session_id: str) -> str:
    return hashlib.sha256(session_id.encode("utf-8")).hexdigest()


def state_path(session_id: str) -> Path:
    return STATE_DIR / f"{session_key(session_id)}.json"


def resolve_snapshot() -> tuple[Path, str]:
    """Locate the current conversation's snapshot and its conversation hash.

    Claude Code exports CLAUDE_CODE_SESSION_ID to the commands it runs; it is
    the same session_id the UserPromptSubmit hook receives, so each
    conversation reads only its own snapshot (as Codex does with
    CODEX_THREAD_ID). There is deliberately no fallback to another
    conversation's file.
    """
    session_id = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not session_id:
        raise SystemExit(
            "Active Time Anchor requires a Claude Code version that exports "
            "CLAUDE_CODE_SESSION_ID. Update Claude Code."
        )
    path = state_path(session_id)
    if not path.exists():
        raise SystemExit(
            "Time Anchor hook snapshot for this conversation is unavailable. "
            "Install and enable the Time Anchor user hook first; it stays silent "
            "inside git projects."
        )
    return path, session_key(session_id)


def utc_offset(value: datetime) -> str:
    total_minutes = int(value.utcoffset().total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def crossed_local_date(previous_local: object, current_local: str) -> bool | None:
    if not isinstance(previous_local, str):
        return None
    previous = datetime.fromisoformat(previous_local)
    current = datetime.fromisoformat(current_local)
    return previous.date() != current.date()


def append_cortex_observation(conversation_hash: str, payload: dict[str, object]) -> None:
    observation = {
        "conversation_hash": conversation_hash,
        "checked_at_local": payload["now_local"],
        "user_prompt_local": payload["user_prompt_local"],
        "elapsed_seconds": payload["elapsed_seconds"],
        "crossed_local_date": payload["crossed_local_date"],
        "snapshot_age_seconds": payload["snapshot_age_seconds"],
    }
    try:
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        with CORTEX_LOG.open("a", encoding="utf-8", newline="\n") as handle:
            json.dump(observation, handle, ensure_ascii=False, separators=(",", ":"))
            handle.write("\n")
    except OSError:
        pass


def main() -> None:
    path, conversation_hash = resolve_snapshot()

    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if snapshot.get("version") != 2 or not isinstance(snapshot.get("now_local"), str):
        raise SystemExit(f"Invalid Time Anchor hook snapshot: {path}")

    looked_at = datetime.now(LOCAL_TZ)
    prompt_time = datetime.fromisoformat(snapshot["now_local"])
    payload: dict[str, object] = {
        "now_local": looked_at.isoformat(timespec="seconds"),
        "timezone": looked_at.tzname() or str(looked_at.tzinfo),
        "utc_offset": utc_offset(looked_at),
        "user_prompt_local": snapshot["now_local"],
        "previous_local": snapshot.get("previous_local"),
        "elapsed_seconds": snapshot.get("elapsed_seconds"),
        "elapsed_human": snapshot.get("elapsed_human"),
        "crossed_local_date": crossed_local_date(
            snapshot.get("previous_local"),
            snapshot["now_local"],
        ),
        "snapshot_age_seconds": round(max(0.0, (looked_at - prompt_time).total_seconds()), 3),
        "state_path": str(path),
        "source": "active read of the current conversation's hook snapshot",
        "temporal_cortex": TEMPORAL_CORTEX_CUE,
    }
    append_cortex_observation(conversation_hash, payload)
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
