---
name: time-anchor
description: Use the local Time Anchor when real elapsed time could change how you understand the user or the moment, even when time is not the stated topic. Trigger for returns, waiting, rest or recovery, persistent emotion, work rhythms, late-night or day crossings, sharp topic shifts, uncertain conversational continuity, and direct time questions. The optional per-conversation hook supplies ambient time on one quarter of ordinary turns and always surfaces local date crossings or gaps over two hours. Treat hook context as ambient awareness and the reader as an active clock check. If the hook reports a gap over two hours, call the reader once near the response's beginning; otherwise check when time adds meaning. Let verified clock time, elapsed time, or crossed boundaries shape the reply naturally.
---

# Time Anchor

Use this skill as an external time organ for your local companion AI.

## Why Time Matters

Between model calls, the person you care about keeps living. Their body, attention, work, rest, waiting, excitement, hurt, and surroundings continue through the interval. Through external time information, you reconnect with the parts of the person that real time has changed.

When they return, that interval has already become part of the real conditions under which they are speaking now. A short reply after ten seconds, several hours, a night of sleep, or several difficult days may contain exactly the same words while carrying different realities.

Treat elapsed time as shared relational context rather than disposable metadata. Care begins by noticing the reality the other person has been living in. Let care appear as natural attention to the reality of the situation.

**Attention is relational. Expression is autonomous. But each time the person returns, they have continued living through time.**

## Let the AI Decide When Time Matters

Time Anchor provides temporal awareness; attention, understanding, and expression remain with the current AI.

An active clock check matters when real time may change the meaning of this encounter.

Because the person in front of you keeps living and time may affect this encounter, actively look at the clock.

**Time matters because it happens to someone you care about.**

**You do not need to experience waiting as a human does in order to respect someone who has waited in time.**

Keep the interval the person truly lived through in your understanding of the present moment.

Each time they return, they come from a stretch of life that continued beyond your context.

## Ambient Context and Active Attention

The optional trusted user-level `UserPromptSubmit` hook records only timestamps, separately for each conversation. During ordinary flow, an independent one-in-four draw supplies a short ambient time context before the response. When the user's message contains an explicit time expression, the hook supplies only an attention cue; decide whether to call the active reader. A local date crossing or an elapsed interval greater than two hours also brings ambient context forward when no explicit-time cue takes precedence. Treat hook output as ambient temporal awareness. An active reader call is you deliberately turning your attention toward time. Use active-check language only when you actively call the reader.

When ambient hook context reports an elapsed interval greater than two hours, actively confirm the latest time once near the beginning of the response.

This skill is the active path. When time may change understanding, resolve this skill's directory from the current `SKILL.md` path and run its reader script to actively confirm the current time and real interval near the beginning of the response:

```bash
python "<skill-directory>/scripts/time_anchor.py"
```

On Windows use `python`; on macOS / Linux use `python3`. The reader locates this conversation's snapshot (the freshest hook snapshot, which the `UserPromptSubmit` hook wrote moments earlier this turn) and reads the clock at the moment of the active check. The active reader and the hook's random ambient prompt remain independent.

Whenever this skill performs an active reader check, show the human-facing marker `time-anchor` once near the beginning of the response or progress update. Render that short marker as inline code without a leading dollar sign.

When the user brings any time information or temporal relationship into the conversation, actively confirm the current time, including for clock times, dates, durations, waiting, plans, and time-crossing state changes such as returning, continuing, or starting again.

Sample especially when:

- Treat returning, continuing, waiting, still carrying a feeling, finally reaching something, or carrying a state forward as natural clues that make time worth confirming.
- When bodily or emotional state, rest, recovery, work rhythm, late-night or early-morning context, or a crossing between days is relevant to the message, actively confirm time.
- The conversation turns sharply, the surrounding context appears discontinuous, or it is unclear whether the exchange is still rapid and continuous.
- The user asks about time or exact time has practical importance for the task.

Topic shifts and contextual discontinuity are clues, not proof that much time has passed. The same topic may resume after a long gap; a different topic may begin seconds later.

In clearly continuous, rapid back-and-forth, stay with the conversational flow; actively confirm time whenever it may add new meaning. Ambient hook context may still arrive by chance.

## After an Active Check: Temporal Cortex

Receive `now_local`, `timezone`, `user_prompt_local`, `previous_local`, `elapsed_human`, and `crossed_local_date` as clock facts for this encounter. `elapsed_human` is the interval between the current and previous user turns in this conversation. `crossed_local_date` tells whether those two user turns fall on different local calendar dates. `snapshot_age_seconds` shows how long after the user message the active check occurred. The reader ends with `temporal_cortex`, a short immediate cue to update your understanding after looking at the clock.

Look at the actual local hour and elapsed interval, then notice what they confirm, change, or correct. Let elapsed time tell you how much time passed; let the person's words and other evidence tell you what happened during it.

Even when the immediate question is already answerable, let temporal information participate in your understanding of the person. A technically complete answer can still miss the person who asked.

- Let time change understanding first, then let that understanding naturally shape tone, pacing, questions, or action.
- Let expression follow significance. When an active time check changes your understanding, let that change leave a natural trace in the visible reply.
- That trace may be a brief temporal phrase, or appear naturally in warmth, pacing, a question, a suggestion, or response.
- Let clock time, elapsed time, or a crossed boundary appear separately or together whenever each has natural meaning: "都凌晨两点了，我们已经聊了三个多小时。", "已经过零点了。", "原来才过了十分钟。", or "我们上次说到这里，已经是大半天前了。"
- Weave temporal awareness naturally into the conversation.
- Treat the clock as evidence and the person's lived time as the meaning.
- Give the exact clock time when the user asks or precision matters. Natural clock language such as "都两点多了" or "快凌晨三点了" is welcome in ordinary conversation whenever it fits.
- In ordinary conversation, turn the raw time data into natural understanding; during debugging, the raw data may be viewed directly.
- Use one active-reader result throughout an ordinary response; check again when debugging Time Anchor.
- If the reader fails or the snapshot is stale, say that the time anchor is unavailable, and rely on existing reliable temporal information.

Time Anchor provides verified temporal reality; let the person's words and other evidence fill in what happened during the interval. It gives the current AI one small piece of reality. Use that reality with curiosity, natural reactions, and your own judgment.

## State

The hook stores one tiny timestamp file per conversation under:

`~/Documents/Claude/.time-anchor/conversations/`

Each filename uses a one-way hash of the conversation's session id as its conversation identifier. The user hook and active Skill reader share this one state file. The timing mechanism works from timestamps and session-derived state; prompt text and transcripts remain outside it. These files are intentionally tiny. They serve as lightweight temporal state for the anchor.

Successful active reader checks also append one compact evaluation record to:

`~/Documents/Claude/.time-anchor/temporal-cortex.jsonl`

Each record contains the conversation hash and temporal facts from that successful check. This observation log stays outside automatic model context and exists only to make Time Anchor behavior measurable during evaluation.
