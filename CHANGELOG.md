# Changelog

All notable public releases of AI Companion Time Anchor are documented here.

## [2.0.0] - 2026-08-10

### Added

- **Temporal Cortex**: the active reader now places a short cognitive-update cue directly beside verified time facts so that looking at the clock can immediately update the agent's understanding before language is produced.
- `crossed_local_date`, a compact derived fact that makes local date crossings explicit without asking the model to infer them from raw timestamps.
- A lightweight local `temporal-cortex.jsonl` observation log for evaluating successful active clock checks without placing the log back into model context.
- Deterministic ambient surfacing for objectively significant transitions: local date crossings and user-turn gaps of two hours or more.
- Stronger active-attention guidance for temporal language and temporal relationships such as returning, continuing, waiting, restarting, dates, durations, and plans.
- A natural temporal-trace principle: when verified time changes the agent's understanding, that change may naturally shape the visible response rather than remaining silently internal.

### Changed

- Ordinary ambient time remains an independent one-in-four draw; significant date crossings and long gaps now bypass the random draw so they are not missed.
- The active reader is now treated as the deliberate clock-check path, with the Temporal Cortex forming a thin bridge from temporal sensing to reasoning.
- Skill language was simplified toward concise, positive behavioral guidance while preserving the tested topic-shift/contextual-discontinuity cue.
- Plugin metadata, README, citation metadata, and release documentation now describe the v2.0 architecture.

### Privacy

The hook still reads only timestamps and session-derived state. It does not inspect prompts or transcripts. Active-reader evaluation records contain only a hashed conversation identifier and temporal facts from the check; all state remains local.

## [1.1.0] - 2026-08-06

### Added

- A verified Codex plugin package that replaces the legacy standalone Skill distribution.
- An optional per-conversation `UserPromptSubmit` hook that records user-turn timestamps and supplies ambient time context on an independent one-in-four draw.
- An active `$time-anchor:time-anchor` Skill that can read the same conversation snapshot when elapsed time may change the meaning of a message.
- Separate clocks for separate conversations using session-scoped snapshots.
- Privacy-preserving hashed conversation identifiers; raw session IDs are not stored.
- A small installer and uninstaller for the user-level hook.
- Machine-readable citation metadata for GitHub and Zenodo through `CITATION.cff`.

### Privacy

The plugin stores timestamp-only local JSON state. It does not store prompts, replies, transcripts, user profiles, raw session IDs, account credentials, or background surveillance data.

## [1.0.0] - 2026-08-04

- First public Windows release.
- Added a lightweight local Skill for current time, previous-call time, and elapsed interval.
- Stored a single local `last_seen.json` file without conversation or user-profile content.
- Published under the MIT License.
