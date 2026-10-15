# Upstream sources

`repos/` contains upstream clones; `skills/` contains the retained personal skills and Codex adaptations. This table records the latest fetched revision (`main` unless noted) and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `2d228630ba1446365f614a108cb8252f1feda202` | `2d228630ba1446365f614a108cb8252f1feda202` |
| Good CSS | https://github.com/vojtaholik/good-css | `repos/good-css` | `92d436ba1937d1b1407c47e35abb3e199eaace2e` | `92d436ba1937d1b1407c47e35abb3e199eaace2e` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `742976ce97f5157b00e67e4a5ece6bc04e1899e3` | `742976ce97f5157b00e67e4a5ece6bc04e1899e3` |
| OpenCode (v2) | https://github.com/anomalyco/opencode | `repos/opencode` | `4617210822bdbb31e5749751afbfb4584ccedac8` | `4617210822bdbb31e5749751afbfb4584ccedac8` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `ce649c03ac3b75b6ae80cbd15b7e2c536caedb5a` | `ce649c03ac3b75b6ae80cbd15b7e2c536caedb5a` |

`skills/design` loads Emil and Good CSS directly. The Poteto directories under `skills/` contain Codex adaptations of the pinned pstack source; see [POTETO.md](POTETO.md) for ownership, exclusions, and refresh rules. Keep source checkouts at their based-on commits. Effect's based-on commit records source considered for its guidance; its provenance retains earlier example revisions. The consuming project's declarations and tests establish available Effect behavior. Matt is no longer an installation dependency; an existing local clone is left untouched.

## Maintenance

For initial installation, use `./scripts/setup.sh`. It clones every missing source at its based-on commit, including Effect, and verifies existing checkouts without fetching or advancing them. The commands below are a separate update workflow.

1. Run `./scripts/sync-repos.sh`. It clones missing sources, pins new Emil, Good CSS, and Poteto clones, and fetches existing ones while preserving their checkouts. Effect tracks `main` with fast-forward updates.
2. For sources managed by the sync script, record each fetched revision using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching. OpenCode's separate `v2` workflow is described below.
3. Before adopting an update, compare its based-on and fetched revisions and inspect the relevant upstream changes and personal skills. Recommend what to adopt and why, preserving personal customizations.
4. When adopting Emil, Good CSS, or Poteto, move the clean checkout and its based-on entry to the same reviewed commit. For Effect, advance the based-on entry when its guidance is adopted into the skill. For Poteto, review and refresh the Codex adaptations and reachable resources per POTETO.md. Skipped updates leave based-on entries unchanged.

OpenCode is a pinned application study for `skills/effect`, with evidence in its [study reference](skills/effect/references/OPENCODE.md). Setup includes this source pin. The sync script does not manage it; fetch updates separately with `git -C repos/opencode fetch origin v2`, preserving the checkout, and review before advancing its based-on revision.
