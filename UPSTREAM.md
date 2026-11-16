# Upstream sources

`repos/` contains upstream clones; `skills/` contains the retained personal skills and Codex adaptations. This table records the latest fetched revision (`main` unless noted) and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `64eb3deb9a5fbfa041faf783e0bc3fd635872e9c` | `64eb3deb9a5fbfa041faf783e0bc3fd635872e9c` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7` | `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7` |
| Benji Taylor | https://github.com/benjitaylor/skills | `repos/benjitaylor` | `299140fafd08df55a9c234e610c3f64af3f45531` | `299140fafd08df55a9c234e610c3f64af3f45531` |

Emil skills are installed under their upstream names, with `$ask-emil` routing to the included specialists. Good CSS and the local Design adapters are removed. Excluded Emil skills remain `ask-sonner`, `pick-ui-library`, `write-swift`, and `animate-expo`. Entry points are regular files; resources and MIT licensing are retained. The Poteto imports follow [POTETO.md](POTETO.md). The Effect skill is version-independent and reads the consuming project’s installed package guidance. It has no upstream release checks or source checkout requirement.

`skills/stageshow` keeps a regular copy of upstream `SKILL.md` so Codex can discover it; setup syncs that file from the adopted pin. Its MIT license, third-party notices, kit, examples, references, and tools remain linked to the unmodified upstream source. Local `agents/openai.yaml` metadata makes invocation explicit-only.

## Maintenance

For installation and routine updates on every machine, run `./scripts/setup.sh` after pulling this collection. It clones missing sources and reconciles clean existing checkouts to their based-on commits. It fetches a pinned commit only when missing locally, preserves branch pointers, and stops on local source edits. `--check` remains read-only. The commands below are the maintainer workflow for fetching and adopting new upstream versions; routine installation does not require them.

1. Run `./scripts/sync-repos.sh`. It clones missing sources at adopted pins and fetches existing sources while preserving their checkouts. Effect is excluded from routine upstream checks and updates.
2. For sources managed by the sync script, record each fetched revision using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching. Fetching a default branch does not adopt it.
3. Use external skill guidance as supplied upstream; no content review is required before adopting updates. Copy included source files exactly and preserve installation exclusions. Only add explicit-invocation metadata in `agents/openai.yaml`.
4. When adopting a source, move its clean checkout and based-on entry to the same adopted commit. Regenerate Emil with `python3 scripts/port_emil.py`. Regenerate Poteto with `python3 scripts/port_poteto.py` per POTETO.md; do not rewrite upstream content. Skipped updates leave based-on entries unchanged.

Application research checkouts are optional maintainer resources. Setup does not clone or require them. Existing clones are preserved.
