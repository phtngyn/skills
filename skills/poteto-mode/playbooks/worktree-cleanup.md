### Worktree and simulator cleanup

1. Record `df -h /` and run `scripts/worktree-audit.sh [-b <base-ref>] [repo-path]` using its absolute path under the installed Poteto mode skill. Use its `--local-only` flag when native PR tools are available and gather PR evidence with those tools. It inventories Git worktrees, not chat sessions.
2. Cross-check every candidate against known active or pinned Codex threads, delegated work, and open PRs. Use [scoped history](../references/codex.md) where available. Hold candidates whose use you cannot establish.
3. Check each worktree’s path, branch, diff, untracked and ignored files, and merge evidence. Treat an unknown PR state or unrelated work as a reason to inspect further.
4. Keep tracked or untracked work unless the user authorized its removal after seeing what would be lost.
5. Remove only the confirmed set with `git worktree remove <path>`. If it refuses because local data remains, inspect and report the files before using force. Prune known stale metadata and verify the result.
6. Include simulator or cache cleanup only when the user requested it. Follow the host device rules and retain active devices and work.

This is the one playbook that deletes user state with no code review to catch a slip, so the gates above are the review.

**Reply:** `df -h /` before and after with space reclaimed, the worktrees pruned, and a one-line reason for each held back (in-use by which chat, or uncommitted work).

Use the [Codex live app and worktree guidance](../references/codex.md) when the host provides the tools.
