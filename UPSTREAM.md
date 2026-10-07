# Upstream sources

Personal skills use these repositories as guidance or direct dependencies, as noted below.

| Source | Repository | Local clone | Last fetched commit (main) | Skills based on commit |
| --- | --- | --- | --- | --- |
| Emil | https://github.com/emilkowalski/skills | `repos/emil` | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` | `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` |
| Effect | https://github.com/Effect-TS/effect | `repos/effect` | `757821fe99b7179f907d6d1a34a4e86de4173112` | `b1d200c40a1dad69def51ebdbf0a1a612a12b8ac` |
| Matt | https://github.com/mattpocock/skills | `repos/mattpocock` | `f3fc5632f401156837ee3872f14fe33ccf1024ea` | Not used yet |
| Poteto | https://github.com/cursor/plugins | `repos/pstack` | `d0ef80d86795816da932a153458c5dbe192d294e` | Not used yet |

`skills/emil` routes directly to the unchanged skills in `repos/emil`. Keep that checkout at the Emil based-on commit; fetch alone must not advance it. `skills/effect` uses the source version cited in its own guide; its local clone may be newer. Matt and Poteto have been explored, but no personal building skills have been written from them yet. Poteto's material is under `pstack/` inside the Cursor plugins repository.

## For future agents

After fetching a repository, update its last fetched commit here from `origin/main`. Fetching does not change the based-on commit.

To assess updates, compare the based-on commit with the last fetched commit, read relevant upstream changes, and inspect our personal skills. Recommend which ideas are worth adopting and why. Preserve our wrappers and customizations. For Emil, adopting an update means advancing the clean upstream checkout and its based-on commit together. For a source not used yet, evaluate it when building the relevant personal skills.

For Emil, advance the based-on commit only when adopting that upstream version, and move the clean checkout to the same commit. If an update is skipped, keep the based-on commit unchanged; add a brief note here only if useful. For original workflows derived from other sources, the based-on commit records the upstream version considered when shaping them.
