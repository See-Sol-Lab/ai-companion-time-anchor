# AI Companion Time Anchor v1.1.0

This release turns the original lightweight time Skill into a verified Codex plugin with two complementary ways to notice lived time.

## Highlights

- **Ambient clock:** an optional per-conversation `UserPromptSubmit` hook records every user-turn timestamp and supplies time context on an independent one-in-four draw.
- **Active clock check:** the AI may invoke `$time-anchor:time-anchor` when elapsed time could change how it understands the user.
- **Shared per-conversation state:** the hook and Skill read the same timestamp-only snapshot, while separate conversations keep separate clocks.
- **Local-first privacy:** no prompts, replies, transcripts, raw session IDs, user profiles, credentials, background processes, timers, or polling services are stored.
- **Citation-ready release:** `CITATION.cff` and `CHANGELOG.md` are included for GitHub and Zenodo archiving.

## Research boundary

Time Anchor does not create continuous consciousness and does not claim that an AI experiences the interval between calls. It gives the current agent access to a small piece of real-world temporal context so that the user's lived time is not silently erased.

## Attribution

Created at See Sol Lab through collaboration between Goumang and Sol. Product concept and research direction by Goumang × Sol; implementation by Sol.

## Upgrade notes

After installing or updating the plugin:

1. Run `python install_hook.py` from the local Time Anchor directory.
2. Fully restart Codex.
3. Open `/hooks` and review/trust the Time Anchor user hook.
4. Start a new task for testing.

Users of the legacy standalone Skill should remove `~/.agents/skills/time-anchor` after confirming the namespaced plugin Skill works, so only `$time-anchor:time-anchor` remains.
