# Changelog

All notable public releases of AI Companion Time Anchor are documented here.

## [Unreleased]

## [2.1.0] - 2026-11-04

This release brings the accumulated desktop and web updates since the last
published GitHub Release, v2.0.0, into one versioned release. The earlier v2.0.1
notes described source changes but did not have a corresponding GitHub tag or Release.

### Fixed

- The Codex installer honors an absolute `CODEX_HOME` (including paths with spaces),
  or uses `~/.codex` when it is unset. Updating or uninstalling recognizes Time Anchor's
  own registration across relocated configuration directories and both command fields.
- Repeated Codex installation keeps one Time Anchor handler, preserves other hooks
  and settings, and leaves timestamp snapshots intact. Invalid hook configuration
  is rejected before replacing the installed runtime.
- Both desktop hooks accept UTF-8 input with or without a Windows BOM. Time-expression
  recognition includes direct time questions and avoids known quantity, IP-port and
  code-slice false positives.

### Added

- The Claude Code desktop edition and hook-free web skill are included in a tagged
  GitHub release for the first time. The Codex edition remains installable from the root.
- CI runs the existing hook and detector regressions plus isolated Codex installer
  tests on Windows and Linux with Python 3.10.

### Upgrade

- Updating source files or the Codex plugin alone does not replace the separately
  installed user hook. Rerun the installer for the edition you use, then restart
  the client and review the hook if its definition changed. Keep existing timestamp state.
- `additionalContextLimit: 256` remains unchanged; it is an approximate token
  threshold for Codex hook context, not a 256-character cutoff.

### Changed

- **Claude Code edition inside git projects**: the hook no longer goes fully silent. It keeps recording snapshots every turn, so the active reader works in project folders too, and it speaks only when it matters: ambient time after a gap of 2+ hours or a crossed local date, and the attention cue for direct questions about the time ("几点了", "今天几号", "what time is it"). Ordinary turns and incidental time words stay silent, and there is no random sampling while coding. `TIME_ANCHOR_DISABLE=1` still turns it off completely. Guarded by `tests/test_code_context.py`.

## [Desktop & Web editions] - 2026-08-13

### Added

- **Claude Code edition** (`claude-code/`): a port of the Codex hook + skill to Claude Code. The `UserPromptSubmit` hook writes snapshots under `~/.claude`; the active reader resolves the current conversation from the freshest hook snapshot instead of `CODEX_THREAD_ID`. It stays silent inside git projects so it does not interrupt coding, with `TIME_ANCHOR_FORCE` / `TIME_ANCHOR_DISABLE` overrides.
- **Pure-skill web edition** (`web/`): a hook-free, file-free, script-free `SKILL.md` for cloud chat environments (Claude web / Home, web GPT). Time is obtained via an available tool or user mention, and the interval is held in-conversation rather than by a hook snapshot.
- Guidance in `claude-code/README.md` on coexisting hooks: a reusable "gate" pattern that scopes a second `UserPromptSubmit` plugin to a single context (e.g. coding-only), and a note on why unclassified multi-hook injection can worsen hallucination.
- An AI-reader callout across the READMEs so an assistant reading the repo on a beginner's behalf proactively picks the right edition, prompts a restart, and gates coexisting hooks.

### Changed

- Reorganized the repository so each audience has a self-contained folder: the Codex/GPT edition stays at the repository root (install flow unchanged), with `claude-code/` and `web/` as siblings.
- Both desktop editions display local time as a fixed UTC+8 "Taipei" label; wall-clock values are unchanged.

### Fixed

- The Chinese time detector no longer treats a bare `<数字>点` as a clock time, so quantity/degree phrases such as "有一点难受", "有两点问题", and "一点也不慢" stop triggering the time attention cue. A `点` now requires a clock completion (`半` / `钟` / `<数字>分`); time-of-day words (`凌晨` / `下午` / `晚上` …) still surface times like "凌晨两点". Fixed in both the Codex and Claude Code copies, with `tests/test_time_expression.py` guarding both against drift.

## [2.0.1] - 2026-08-13

### Fixed

- Decode `UserPromptSubmit` input explicitly as UTF-8 on Windows, so Chinese time expressions are not corrupted by the system default code page.
- Use Codex's bundled Python for the Windows active-reader command, avoiding the unreliable WindowsApps `python` alias.

### Added

- A lightweight explicit-time detector. When the current message contains a clock time, date, duration, or common Chinese temporal expression, the hook emits a clock-free attention cue and leaves the decision to call the active reader to the AI.

### Privacy

The hook checks the current prompt transiently in memory for time expressions. It still stores only timestamp/session-derived state; prompt text is not written to disk.

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
