# Time Anchor v2.1.0 — Reliable upgrades across desktop editions

This release packages the accumulated changes since the last published GitHub
Release, v2.0.0. Source metadata had previously advanced to v2.0.1 without a
corresponding GitHub tag or Release. v2.1.0 gives users a versioned download of
the current Codex, Claude Code and hook-free web editions.

## Highlights

- **Codex installation and upgrades:** honor an absolute `CODEX_HOME`, defaulting
  to `~/.codex`; recognize existing Time Anchor registrations in relocated config
  directories; keep a single registration on repeated installation; preserve
  unrelated hooks, configuration and timestamp snapshots.
- **Fail clearly before updating:** invalid Codex hook configuration is rejected
  before replacing the installed runtime. A relative `CODEX_HOME` gets an explicit error.
- **Windows input:** both desktop hooks accept UTF-8 with or without a BOM.
- **Time-expression detection:** accumulated fixes reduce quantity, IP-port and
  code-slice false positives and recognize direct questions about the time.
- **Claude Code in coding projects:** snapshots are still recorded every turn.
  In a git project, ordinary turns and incidental time words remain quiet; long
  gaps, date crossings and direct time questions can surface time context.
  `TIME_ANCHOR_DISABLE=1` disables the hook; `TIME_ANCHOR_FORCE=1` uses chat behaviour.
- **Three editions:** use the root for local Codex, `claude-code/` for local
  Claude Code, and `web/` for the hook-free cloud-chat skill.
- **Regression coverage:** hook input, time expressions, coding-project behaviour
  and isolated Codex install/update/uninstall checks run on Windows and Linux in CI.

## Upgrade existing installations

Updating a Git checkout or the Codex plugin does not automatically replace the
separately installed user hook.

1. Update/download v2.1.0 and choose the edition you actually use. For Codex,
   install/update the Time Anchor plugin Skill as well; its hook installer does
   not install the plugin.
2. For Codex, run `python install_hook.py` from the repository root. Keep the same
   `CODEX_HOME` you use to launch Codex, if set.
3. For Claude Code, run `python install_hook.py` from `claude-code/`. Keep your
   existing `CLAUDE_CONFIG_DIR`, if set.
4. Restart that client. Review/trust Time Anchor if the client reports a changed
   hook definition. Existing trust decisions are not fabricated by the installers.
5. Keep the existing timestamp directory. Send a real message and use the active
   reader to verify that this conversation's snapshot advances. The first message
   in a conversation with no prior snapshot has no earlier interval to report.

The default Codex hook budget remains `additionalContextLimit: 256`, an approximate
token threshold, not a 256-character cutoff.

## Privacy and compatibility

Python 3.10 or newer is required. Local snapshots retain the same version-2 format
and location. Prompt text is inspected transiently for time expressions or context
selection; prompts and replies are not stored by the timing mechanism. State and
active-reader evaluation records remain local. No background updater is installed.

The existing DOI in `CITATION.cff` is the all-versions Zenodo identifier. A
version-specific v2.1.0 archive identifier should be recorded after archival succeeds;
it is not implied merely by publishing this release.
