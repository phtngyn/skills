### Worktree cleanup

1. Inventory with `git worktree list --porcelain`, git status, merge ancestry, PR state, disk usage, and live owned processes. Read the actual paths from git. Do not infer age or safety from directory names or transcript modification times.
2. Classify worktrees as active, dirty, unmerged, merged, or uncertain. A closed PR alone is not proof its work was merged. Preserve unique commits and uncommitted changes.
3. Present concrete deletion candidates with the evidence for each. Remove only candidates covered by the user's cleanup authorization. Prefer `git worktree remove` and `git worktree prune`; do not force-remove a dirty tree without explicit authorization.
4. Audit submodules and shared resources before removal. Stop only owned processes tied to approved candidates. Recheck reclaimed space and git's remaining worktree inventory.
5. Treat simulator or cache deletion as separate cleanup scope. List exact candidates and contents before any authorized removal; never sweep application data or all simulator devices as a generic disk-saving step.

Reply with removed paths, reclaimed space, preserved work, and uncertain candidates.
