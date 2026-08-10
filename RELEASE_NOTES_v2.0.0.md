# AI Companion Time Anchor v2.0.0 — Temporal Cortex

Time Anchor v2.0 extends the original two-path time anchor into a lightweight temporal pipeline: ambient awareness, deliberate clock checks, and a thin **Temporal Cortex** between verified time facts and the agent's next judgment.

## DOI

- **All versions / Concept DOI:** `10.5281/zenodo.21815643` — resolves to the latest published version.
- **v2.0.0 version DOI:** `10.5281/zenodo.21875047`.

## Highlights

- **Temporal Cortex:** successful active clock checks now end with an immediate cognitive-update cue, encouraging the agent to let verified temporal facts update its understanding before it responds.
- **Derived date-crossing fact:** the active reader exposes `crossed_local_date` alongside current time, previous user-turn time, elapsed time, and snapshot age.
- **Significant ambient transitions:** ordinary turns keep the independent one-in-four ambient draw, while local date crossings and gaps of two hours or more always surface ambient time context.
- **Natural temporal traces:** the Skill explicitly encourages a changed temporal understanding to leave a natural trace in the visible response without turning every reply into a timestamp report.
- **Broader temporal attention:** clock times, dates, durations, waiting, plans, returning, continuing, restarting, and similar temporal relationships can invite an active check.
- **Lightweight evaluation log:** successful active checks append compact temporal facts to `~/Documents/Codex/.time-anchor/temporal-cortex.jsonl`. The log is not automatically injected into model context.

## Architecture

### Ambient Hook — peripheral awareness

The per-conversation `UserPromptSubmit` hook continues to record every user-turn timestamp. On ordinary turns, ambient time appears on an independent one-in-four draw. Local date crossings and gaps of two hours or more bypass the random draw because they are objectively significant temporal transitions.

The hook continues to operate from timestamps and session-derived state only; it does not inspect prompt text.

### Active Reader — deliberately looking at the clock

The active Skill reads the current conversation snapshot and the live local clock. It can provide:

- `now_local`
- `timezone`
- `user_prompt_local`
- `previous_local`
- `elapsed_seconds`
- `elapsed_human`
- `crossed_local_date`
- `snapshot_age_seconds`

This remains distinct from ambient hook context: an active reader call is the deliberate clock-check path.

### Temporal Cortex — perception into understanding

The reader places a short `temporal_cortex` cue directly beside the verified temporal facts:

> Let this time check update your understanding of the moment. If the temporal facts change what this situation means, let that change naturally shape your response.

The Temporal Cortex does not infer what happened during the interval and does not assign emotion or meaning on behalf of the model. It is intentionally thin: verified facts arrive first; the cue makes the act of looking at the clock immediately relevant to the next reasoning step; interpretation remains with the current AI.

## Why v2.0

v1.1 solved temporal availability: the model could receive ambient time and could deliberately read the clock.

v2.0 addresses the next failure mode observed in real use: **silent consumption**. An agent could actively check time, correctly update an internal judgment, and still suppress every visible trace of that changed understanding. The Temporal Cortex is designed as a minimal bridge from temporal sensing to cognition rather than another large rules engine.

## Privacy and local state

Per-conversation snapshots remain under:

```text
~/Documents/Codex/.time-anchor/conversations/
```

Successful active checks may append an evaluation record to:

```text
~/Documents/Codex/.time-anchor/temporal-cortex.jsonl
```

The evaluation record contains only a hashed conversation identifier and temporal facts from the successful check. Prompts, replies, transcripts, user profiles, raw session IDs, account credentials, and message text are not stored by the timing mechanism.

## Research boundary

Time Anchor does not create continuous consciousness and does not claim that an AI experiences the interval between calls. Temporal Cortex is not a user-state classifier or surveillance layer. It gives the current agent a small amount of verified temporal reality and a lightweight path for that reality to participate in understanding.

## Attribution

Created at See Sol Lab through collaboration between Goumang and Sol. Product concept and research direction by Goumang × Sol; implementation by Sol.

## Upgrade notes

After updating to v2.0.0:

1. Run `python install_hook.py` again so the installed user-level hook matches the v2.0 source.
2. Fully restart Codex.
3. Open `/hooks` and review/trust the Time Anchor `UserPromptSubmit` hook if needed.
4. Start a fresh task or conversation for clean testing.
5. A successful active check should expose `crossed_local_date` and `temporal_cortex`; the local evaluation log will appear after successful active reader calls.

Users of the legacy standalone Skill should keep only the namespaced plugin Skill `$time-anchor:time-anchor`.
