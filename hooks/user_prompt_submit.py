from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sys
import tempfile
from datetime import datetime
from pathlib import Path


STATE_DIR = Path.home() / "Documents" / "Codex" / ".time-anchor" / "conversations"
LONG_GAP_SECONDS = 2 * 60 * 60
TIME_EXPRESSION = re.compile(
    r"(?:"
    r"\d{1,2}:\d{2}|"
    r"[零〇一二两三四五六七八九十百\d]+点(?:半|[零〇一二两三四五六七八九十\d]+分)?|"
    r"[零〇一二两三四五六七八九十百\d]+(?:秒钟?|分钟|小时|天|周|星期|个月|年)|"
    r"[零〇一二两三四五六七八九十百\d]+月[零〇一二两三四五六七八九十百\d]+(?:日|号)|"
    r"今天|昨天|明天|前天|后天|现在|刚才|刚刚|一会儿|等会儿|"
    r"凌晨|早上|上午|中午|下午|傍晚|晚上|夜里|半夜"
    r")"
)


def local_now() -> datetime:
    return datetime.now().astimezone()


def utc_offset(value: datetime) -> str:
    total_minutes = int(value.utcoffset().total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def elapsed_human(seconds: float) -> str:
    total = max(0, round(seconds))
    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    return " ".join(parts)


def state_path(session_id: str) -> Path:
    session_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    return STATE_DIR / f"{session_key}.json"


def load_previous(path: Path) -> datetime | None:
    if not path.exists():
        return None
    state = json.loads(path.read_text(encoding="utf-8"))
    current = state.get("now_local")
    if not isinstance(current, str):
        raise ValueError(f"Invalid time-anchor state: {path}")
    return datetime.fromisoformat(current)


def write_state(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f"{path.stem}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def ambient_context(payload: dict[str, object]) -> str:
    previous = payload["previous_local"]
    if previous is None:
        interval = "No previous user-turn timestamp is available yet."
    else:
        interval = (
            f"Previous user-turn time in this Codex conversation: {previous}; "
            "elapsed between user turns in this conversation: "
            f"{payload['elapsed_human']}."
        )
    return (
        "[Time Anchor ambient context — automatically supplied by the optional hook] "
        f"Current local user-turn time: {payload['now_local']} "
        f"({payload['timezone']}, UTC{payload['utc_offset']}). {interval} "
        "This is environmental context, not an active clock check. Let it shape the response "
        "naturally when relevant; reserve active-check language for moments when you deliberately "
        "call the reader."
    )


def time_attention_context() -> str:
    return (
        "[Time Anchor attention cue] The user's message contains explicit time information. "
        "Decide whether to actively call the Time Anchor reader."
    )


def main() -> None:
    event = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    if event.get("hook_event_name") != "UserPromptSubmit":
        raise ValueError("time-anchor hook requires UserPromptSubmit input")
    session_id = event.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("time-anchor hook requires a session_id")
    prompt = event.get("prompt")
    if not isinstance(prompt, str):
        raise ValueError("time-anchor hook requires a prompt")
    now = local_now()
    path = state_path(session_id)
    previous = load_previous(path)
    elapsed_seconds = None if previous is None else max(0.0, (now - previous).total_seconds())
    crossed_local_date = None if previous is None else previous.date() != now.date()
    payload: dict[str, object] = {
        "version": 2,
        "now_local": now.isoformat(timespec="seconds"),
        "timezone": now.tzname() or str(now.tzinfo),
        "utc_offset": utc_offset(now),
        "previous_local": None if previous is None else previous.isoformat(timespec="seconds"),
        "elapsed_seconds": None if elapsed_seconds is None else round(elapsed_seconds, 3),
        "elapsed_human": None if elapsed_seconds is None else elapsed_human(elapsed_seconds),
        "crossed_local_date": crossed_local_date,
    }
    write_state(path, payload)

    explicit_time = TIME_EXPRESSION.search(prompt) is not None
    significant_transition = bool(crossed_local_date) or (
        elapsed_seconds is not None and elapsed_seconds >= LONG_GAP_SECONDS
    )
    if explicit_time:
        additional_context = time_attention_context()
    else:
        additional_context = ambient_context(payload)
    if not significant_transition and secrets.randbelow(4) != 0:
        if not explicit_time:
            return

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }
    json.dump(output, sys.stdout, ensure_ascii=True, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
