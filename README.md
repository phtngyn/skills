# Personal skills

A Codex-only collection of personal workflows and entry points backed by tracked upstream sources.

## Emil

Use `/emil <prompt>` through Codex's skill picker, or explicitly name `$emil` in a prompt. The entry point owns design exploration, UI implementation, motion, critique, mobile polish, and UI stress checks. Upstream skills and their references load only when relevant.

Examples:

```text
/emil this settings screen feels crowded. Recommend a direction before changing it.
/emil explore three different versions of this pricing card.
/emil implement the selected version and verify its interactions.
/emil make this drawer feel responsive without adding unnecessary motion.
/emil review this component with long labels, empty data, and a narrow viewport.
```

The wrapper lives in `skills/emil`. It routes directly to Emil's unchanged upstream skills through `skills/emil/upstream`, a link to `repos/emil/skills`. Keep that checkout available at the commit recorded in [UPSTREAM.md](UPSTREAM.md). There are no rewritten supporting guides.

A user-level symlink at `~/.agents/skills/emil` makes the wrapper available to Codex. Start a new chat if the skill picker has not refreshed. Follow-ups continue the design task without setting an application-wide mode.

## Upstream maintenance

`repos/` contains upstream clones; `skills/` contains our personal workflows and wrappers. [UPSTREAM.md](UPSTREAM.md) records each source repository, its last fetched commit, and the commit our skills are based on. Future agents compare those commits and recommend whether our skills should change.

`scripts/sync-repos.sh` fetches Emil updates without advancing its existing checkout. New Emil clones are checked out at the recorded based-on commit. After syncing, record the fetched `origin/main` commit in `UPSTREAM.md`; adopt it only after reviewing the changes.
