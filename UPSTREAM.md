# Upstream sources

`repos/` contains upstream clones; `skills/` contains our personal workflows and wrappers. This table records the latest fetched `main` revision and the revision each skill uses.

| Source | Repository | Local clone | Last fetched commit (main) | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` |
| Good CSS | https://github.com/vojtaholik/good-css | `repos/good-css` | `e6174b7a720f58c8e7e997eec559ab8bd6fc44df` | `e6174b7a720f58c8e7e997eec559ab8bd6fc44df` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `757821fe99b7179f907d6d1a34a4e86de4173112` | `757821fe99b7179f907d6d1a34a4e86de4173112` |
| Matt | https://github.com/mattpocock/skills | `repos/mattpocock` | `f3fc5632f401156837ee3872f14fe33ccf1024ea` | `f3fc5632f401156837ee3872f14fe33ccf1024ea` |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `d0ef80d86795816da932a153458c5dbe192d294e` | `d0ef80d86795816da932a153458c5dbe192d294e` |

`skills/emil` loads Emil directly and uses `skills/good-css` for CSS techniques from Good CSS; `skills/build` loads Matt and Poteto directly. Keep these checkouts at their based-on commits. Poteto's material is under `repos/pstack/pstack`. Effect's based-on commit records source considered for its guidance; its provenance retains earlier example revisions. Its checkout may be newer, so agents compare it with the consuming package before trusting API facts.

## Maintenance

1. Run `./scripts/sync-repos.sh`. It clones missing sources, pins new Emil, Good CSS, Matt, and Poteto clones, and fetches existing ones while preserving their checkouts. Effect tracks `main` with fast-forward updates.
2. Record each fetched revision in the table using `git -C <local-clone> rev-parse origin/main`. Keep based-on commits unchanged during fetching.
3. Before adopting an update, compare its based-on and fetched revisions and inspect the relevant upstream changes and personal skills. Recommend what to adopt and why, preserving personal customizations.
4. When adopting Emil, Good CSS, Matt, or Poteto, move the clean checkout and its based-on entry to the same reviewed commit. For Effect, advance the based-on entry when its guidance is adopted into the skill. Skipped updates leave based-on entries unchanged.
