# Upstream sources

`repos/` contains upstream clones; `skills/` contains the retained personal skills and Codex adaptations. This table records the latest fetched revision (`main` unless noted) and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `2d228630ba1446365f614a108cb8252f1feda202` | `2d228630ba1446365f614a108cb8252f1feda202` |
| Good CSS | https://github.com/vojtaholik/good-css | `repos/good-css` | `92d436ba1937d1b1407c47e35abb3e199eaace2e` | `92d436ba1937d1b1407c47e35abb3e199eaace2e` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `e62a149ee10760c72c74086e1921d2da5b9b6c76` | `3b28bf686bf26e9700edd39c025aff2744dc5303` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `8b3326d99fd4b993cb33a24dad8af03175c642c5` | `8b3326d99fd4b993cb33a24dad8af03175c642c5` |

`skills/design` loads Emil and Good CSS directly. The Poteto directories under `skills/` contain Codex adaptations of the pinned pstack source; see [POTETO.md](POTETO.md) for ownership, exclusions, and refresh rules. Keep source checkouts at their based-on commits. Effect's based-on commit matches the reviewed stable release. Its maintenance and historical research live outside the installed skill in [research/effect](research/effect/MAINTENANCE.md). The consuming project's declarations and tests establish available Effect behavior. Matt is no longer an installation dependency; an existing local clone is left untouched.

## Maintenance

For initial installation, use `./scripts/setup.sh`. It clones every missing source at its based-on commit, including Effect, and verifies existing checkouts without fetching or advancing them. The commands below are a separate update workflow.

1. Run `./scripts/sync-repos.sh`. It clones missing sources at adopted pins and fetches existing sources while preserving their checkouts, including Effect.
2. For sources managed by the sync script, record each fetched revision using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching. Fetching a default branch does not adopt it.
3. Before adopting an update, compare its based-on and fetched revisions and inspect the relevant upstream changes and personal skills. Recommend what to adopt and why, preserving personal customizations.
4. When adopting a source, move its clean checkout and based-on entry to the same reviewed commit. For Effect, verify the registry's latest stable release, resolve its release tag, and validate against the published package before adopting; do not use unreleased `main` behavior as the skill baseline. For Poteto, review and refresh the Codex adaptations and reachable resources per POTETO.md. Skipped updates leave based-on entries unchanged.

Application research checkouts are optional maintainer resources, recorded in [research/effect](research/effect/MAINTENANCE.md). Setup does not clone or require them. Existing clones are preserved.
