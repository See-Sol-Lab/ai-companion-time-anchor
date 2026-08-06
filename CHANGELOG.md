# Changelog

All notable public releases of AI Companion Time Anchor are documented here.

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
