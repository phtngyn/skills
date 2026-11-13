# Upstream sources

`repos/` contains upstream clones; `skills/` contains the retained personal skills and Codex adaptations. This table records the latest fetched revision (`main` unless noted) and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `0f2e23b32bb1265e84cff8d3e75785fec953fb1b` | `0f2e23b32bb1265e84cff8d3e75785fec953fb1b` |
| Good CSS | https://github.com/vojtaholik/good-css | `repos/good-css` | `35e0e8c673854ca34d8e1879038e44834c855dfb` | `35e0e8c673854ca34d8e1879038e44834c855dfb` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `f9f5f9de9431a6ac47b249a443ba999c67c35ac2` | `289a53f7b1fc40049219c6e69022db2fb859c356` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `05b49176bc9e00d8e9e3dbf136fa76631cd6468a` | `2776ddd2355d6d6c8747d3964600f28daf62f049` |
| Benji Taylor | https://github.com/benjitaylor/skills | `repos/benjitaylor` | `299140fafd08df55a9c234e610c3f64af3f45531` | `299140fafd08df55a9c234e610c3f64af3f45531` |

`skills/design` coordinates fifteen local `design-*` Codex adapters that load Emil and Good CSS directly. This family maintains its own workflow and source rules; see [Design ownership](skills/design/PROVENANCE.md). The Poteto directories under `skills/` contain Codex adaptations of the pinned pstack source; see [POTETO.md](POTETO.md) for ownership, exclusions, and refresh rules. Keep source checkouts at their based-on commits. Effect's based-on commit matches the reviewed stable release. Its maintenance and historical research live outside the installed skill in [research/effect](research/effect/MAINTENANCE.md). The consuming project's declarations and tests establish available Effect behavior. Matt is no longer an installation dependency; an existing local clone is left untouched.

`skills/stageshow` links the complete, unmodified upstream Stageshow folder, including its MIT license, third-party notices, kit, examples, references, and tools. Local `agents/openai.yaml` metadata makes invocation explicit-only.

## Maintenance

For installation and routine updates on every machine, run `./scripts/setup.sh` after pulling this collection. It clones missing sources and reconciles clean existing checkouts to their based-on commits, including Effect. It fetches a pinned commit only when missing locally, preserves branch pointers, and stops on local source edits. `--check` remains read-only. The commands below are the maintainer workflow for fetching and adopting new upstream versions; routine installation does not require them.

1. Run `./scripts/sync-repos.sh`. It clones missing sources at adopted pins and fetches existing sources while preserving their checkouts. Effect is excluded from routine upstream checks and updates.
2. For sources managed by the sync script, record each fetched revision using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching. Fetching a default branch does not adopt it.
3. Use external skill guidance as supplied upstream; no content review is required before adopting updates. Preserve the existing local adapters and exclusions.
4. When adopting a source, move its clean checkout and based-on entry to the same adopted commit. Leave Effect at its existing pin unless an Effect update is explicitly requested. For Poteto, review the minimal substitutions and regenerate the retained skills with `scripts/port_poteto.py` per POTETO.md. Skipped updates leave based-on entries unchanged.

Application research checkouts are optional maintainer resources, recorded in [research/effect](research/effect/MAINTENANCE.md). Setup does not clone or require them. Existing clones are preserved.
