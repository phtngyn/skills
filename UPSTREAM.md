# Upstream sources

`repos/` contains upstream clones; `skills/` contains the retained personal skills and Codex adaptations. This table records the latest fetched revision (`main` unless noted) and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `c8a79627b59d72d764d6ab6f2c87c09a48169833` | `c8a79627b59d72d764d6ab6f2c87c09a48169833` |
| Good CSS | https://github.com/vojtaholik/good-css | `repos/good-css` | `35e0e8c673854ca34d8e1879038e44834c855dfb` | `35e0e8c673854ca34d8e1879038e44834c855dfb` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `cb679e39cabeeadc5b40a5e20da311b9e4054a1b` | `506eef143bcc1750ce58920aac1e45da7265d103` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `2776ddd2355d6d6c8747d3964600f28daf62f049` | `2776ddd2355d6d6c8747d3964600f28daf62f049` |
| Benji Taylor | https://github.com/benjitaylor/skills | `repos/benjitaylor` | `299140fafd08df55a9c234e610c3f64af3f45531` | `299140fafd08df55a9c234e610c3f64af3f45531` |

`skills/design` coordinates fourteen local `design-*` Codex adapters that load Emil and Good CSS directly. This family maintains its own workflow and source rules; see [Design ownership](skills/design/PROVENANCE.md). The Poteto directories under `skills/` contain Codex adaptations of the pinned pstack source; see [POTETO.md](POTETO.md) for ownership, exclusions, and refresh rules. Keep source checkouts at their based-on commits. Effect's based-on commit matches the reviewed stable release. Its maintenance and historical research live outside the installed skill in [research/effect](research/effect/MAINTENANCE.md). The consuming project's declarations and tests establish available Effect behavior. Matt is no longer an installation dependency; an existing local clone is left untouched.

`skills/stageshow` links the complete, unmodified upstream Stageshow folder, including its MIT license, third-party notices, kit, examples, references, and tools.

## Maintenance

For installation and routine updates on every machine, run `./scripts/setup.sh` after pulling this collection. It clones missing sources and reconciles clean existing checkouts to their based-on commits, including Effect. It fetches a pinned commit only when missing locally, preserves branch pointers, and stops on local source edits. `--check` remains read-only. The commands below are the maintainer workflow for reviewing and adopting new upstream versions; routine installation does not require them.

1. Run `./scripts/sync-repos.sh`. It clones missing sources at adopted pins and fetches existing sources while preserving their checkouts, including Effect.
2. For sources managed by the sync script, record each fetched revision using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching. Fetching a default branch does not adopt it.
3. Before adopting an update, compare its based-on and fetched revisions and inspect the relevant upstream changes and personal skills. Recommend what to adopt and why, preserving personal customizations.
4. When adopting a source, move its clean checkout and based-on entry to the same reviewed commit. For Effect, verify the registry's latest stable release, resolve its release tag, and validate against the published package before adopting; do not use unreleased `main` behavior as the skill baseline. For Poteto, review the minimal substitutions and regenerate the retained skills with `scripts/port_poteto.py` per POTETO.md. Skipped updates leave based-on entries unchanged.

Application research checkouts are optional maintainer resources, recorded in [research/effect](research/effect/MAINTENANCE.md). Setup does not clone or require them. Existing clones are preserved.
