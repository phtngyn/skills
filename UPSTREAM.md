# Upstream sources

`repos/` contains upstream clones; `skills/` contains our personal workflows and wrappers. This table records the latest fetched `main` revision and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit (main) | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `2d228630ba1446365f614a108cb8252f1feda202` | `2d228630ba1446365f614a108cb8252f1feda202` |
| Good CSS | https://github.com/vojtaholik/good-css | `repos/good-css` | `92d436ba1937d1b1407c47e35abb3e199eaace2e` | `92d436ba1937d1b1407c47e35abb3e199eaace2e` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `8aee3b9caa796aa79316c82c7c83f98c89dc49f5` | `757821fe99b7179f907d6d1a34a4e86de4173112` |
| Matt | https://github.com/mattpocock/skills | `repos/mattpocock` | `49dd158d1076134a641b33efb035946536778336` | `49dd158d1076134a641b33efb035946536778336` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def` | `1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def` |

`skills/design` loads Emil and Good CSS directly; `skills/build` loads Matt and Poteto directly. `skills/write` independently loads Matt's writing guidance. `skills/bro` and `skills/ketchup` contain unchanged copies of Poteto's original instructions and remain manual-only. Review adopted Poteto changes against the local integration rules and refresh both copies from the adopted checkout. Keep these checkouts at their based-on commits. Poteto's material is under `repos/pstack/pstack`. Effect's based-on commit records source considered for its guidance; its provenance retains earlier example revisions. Its checkout may be newer, so agents compare it with the consuming package before trusting API facts.

## Maintenance

For initial installation, use `./scripts/setup.sh`. It clones every missing source at its based-on commit, including Effect, and verifies existing checkouts without fetching or advancing them. The commands below are a separate update workflow.

1. Run `./scripts/sync-repos.sh`. It clones missing sources, pins new Emil, Good CSS, Matt, and Poteto clones, and fetches existing ones while preserving their checkouts. Effect tracks `main` with fast-forward updates.
2. Record each fetched revision in the table using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching.
3. Before adopting an update, compare its based-on and fetched revisions and inspect the relevant upstream changes and personal skills. Recommend what to adopt and why, preserving personal customizations.
4. When adopting Emil, Good CSS, Matt, or Poteto, move the clean checkout and its based-on entry to the same reviewed commit. For Effect, advance the based-on entry when its guidance is adopted into the skill. For Poteto, also refresh the unchanged Bro and Ketchup copies and verify they match the adopted source. Skipped updates leave based-on entries unchanged.
