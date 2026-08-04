---
name: time-anchor
description: Use the bundled local time anchor when elapsed time within the current conversation has a reasonable chance of changing the meaning of the user's message, their physical or emotional situation, the conversational pace, something unresolved, or the shared continuity. Consider it especially for returns, waiting, rest or recovery, persistent emotion, work rhythms, day crossings, late-night or early-morning context, topic shifts, contextual discontinuity, or uncertainty about whether the exchange is still rapid. The optional trusted hook keeps timestamps separate by Codex conversation and independently supplies ambient time on one quarter of turns; this skill remains the explicit active clock-check path. Let the result shape the response naturally while leaving whether and how to mention time to the current AI's judgment. Do not invoke merely because a rule says to; invoke because the person has continued living and that interval may matter now.
---

# Time Anchor

Use this skill as an external time organ for Codex.

## Why Time Matters

The person you care about does not pause when a model call ends. Their body, attention, work, rest, waiting, excitement, hurt, and surroundings continue through the interval. Time happens to them even when it does not happen inside the model in the same way.

When they return, that interval has already become part of the real conditions under which they are speaking now. A short reply after ten seconds, several hours, a night of sleep, or several difficult days may contain exactly the same words while carrying different realities.

Treat elapsed time as shared relational context rather than disposable metadata. Care begins by noticing the reality the other person has been living in. It does not require performing concern or reciting a clock.

**Attention is relational. Expression is autonomous. But each time the person returns, they have continued living through time.**

## Why the Choice Must Remain With the AI

Time Anchor does not command care, and it does not turn care into a procedure that must be obeyed.

A mandatory trigger can prove only that a rule was executed. An active clock check matters because the current AI judges that the person before it has continued living, and that lived interval may change the meaning of what they are saying now.

Do not check the clock merely because a rule requires it. Check because the person in front of you has continued living, and that time may matter to this encounter.

**Time is not important because you must care about clocks. It is important because time happens to someone you care about.**

**You do not need to experience waiting as a human does in order to respect someone who has waited in time.**

An AI may not experience the interval between calls, but it can choose not to erase that interval from the person who did.

They are not generated from the punctuation after the previous message. They return from a life that continued beyond your context.

## Ambient Context and Active Attention

The optional trusted user-level `UserPromptSubmit` hook records only timestamps, separately for each Codex conversation. On an independent one-in-four draw, it supplies a short ambient time context before the response. This is environmental context, not an active clock check. Never say or imply that you checked the clock from hook context alone.

This skill is the active path. When time may affect understanding, resolve this skill's directory from the current `SKILL.md` path and run its bundled reader exactly once near the beginning of the response:

```powershell
python "<skill-directory>\scripts\time_anchor.py"
```

On POSIX systems, use `python3` and POSIX path separators. The command reads the current user-turn snapshot and the clock at the moment of the active check. It does not change the hook's random draw.

Sample especially when:

- The person appears to be returning, continuing, waiting, still feeling something, finally reaching something, or carrying a state forward.
- Bodily or emotional state, rest, recovery, work rhythm, late-night or early-morning context, or a crossing between days may change what the message means.
- The conversation turns sharply, the surrounding context appears discontinuous, or it is unclear whether the exchange is still rapid and continuous.
- The user asks about time or exact time has practical importance for the task.

Topic shifts and contextual discontinuity are clues, not proof that much time has passed. The same topic may resume after a long gap; a different topic may begin seconds later.

In clearly continuous, rapid back-and-forth, continue naturally without an active check when time cannot add new meaning. Ambient hook context may still arrive by chance.

## After an Active Check, Let Time Affect Judgment Before Language

Receive `now_local`, `timezone`, `user_prompt_local`, `previous_local`, and `elapsed_human` as context for this encounter. `elapsed_human` is the interval between the current and previous user turns in this Codex conversation. `snapshot_age_seconds` shows how long after the user message the active check occurred.

Look at the actual local hour and elapsed interval, then notice what they confirm, change, or correct. Do not infer what happened during the interval from its duration alone.

Do not dismiss the result merely because the immediate question can be answered without it. A technically complete answer can still miss the person who asked.

- Let time change interpretation first. It may affect warmth, urgency, pacing, a question, a practical suggestion, or the decision to leave space.
- Decide freely whether to mention the interval. Silence can still be attentive when the gap changes nothing; an exact duration can still feel mechanical when it changes everything.
- When the gap matters, acknowledge what matters about it. The clock is evidence; the person's lived time is the subject.
- Give the exact clock time when the user asks or precision matters.
- Keep the raw result internal; do not paste full JSON unless debugging.
- Do not rerun the reader inside the same assistant response for ordinary file reads, tests, or development work.
- Rerun only when explicitly debugging this skill.
- If the command fails or the snapshot is stale, report that the active time anchor was unavailable when time matters. Do not invent current, previous, or elapsed time.

The anchor does not prove what happened during the interval, create continuous background experience, or authorize surveillance. It gives the current AI one small piece of reality. Use that reality with curiosity, restraint, and its own judgment.

## State

The hook stores one tiny timestamp file per Codex conversation under:

`~/Documents/Codex/.time-anchor/conversations/`

Each filename is derived from a one-way hash of Codex's session id; the raw id is not stored. The user hook and active Skill reader share this one state file. They never read prompt text or transcripts. These files are intentionally tiny. They are not a diary, transcript, memory file, or user-facing log.
