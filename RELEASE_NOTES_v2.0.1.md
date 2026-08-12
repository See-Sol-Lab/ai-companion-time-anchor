# Time Anchor v2.0.1

This maintenance release repairs explicit-time attention on Windows.

- `UserPromptSubmit` input is decoded as UTF-8, preventing Chinese time words from turning into mojibake before matching.
- Explicit clock times, dates, durations, and common Chinese temporal expressions now raise a short attention cue. The cue contains no clock answer; the AI still decides whether to invoke the active reader.
- The Windows Skill command now uses Codex's bundled Python rather than the unreliable WindowsApps alias.

The hook examines the current prompt transiently for time expressions. Prompt text is not stored; local state remains timestamp/session-derived only.
