### Opening a PR

Use this delivery step when the user's task includes a PR. Otherwise leave a verified local change and report it.

1. Inspect git status and the actual base branch. Preserve unrelated work. Use a separate worktree when isolation is needed. Give parallel writers separate owned worktrees; never reset a dirty checkout to recover from a collision.
2. Review the diff for dead code, unnecessary layers, and accidental changes. Run `no-comments`, and use `technical-writing` and `unslop` for delivery prose. Verify the committed or proposed head with the checks appropriate to the change.
3. Follow the repository's commit and PR conventions. Prefer small coherent commits and PRs. For a stack, each child targets its parent branch, and every layer carries its own evidence. Do not create a stack just to split a trivial change.
4. Use an available PR tool or `gh`, within existing publication authority. Write multiline bodies through structured arguments or a body file. Lead with the problem and resulting behavior, then describe meaningful changes and actual verification. Keep exhaustive logs in linked artifacts.
5. Register each PR through the host's linking tool when available, immediately after creation or starting work on it. Reconcile linked PRs before completion. Do not claim linkage if the tool fails.
6. Read back the actual PR state. Honor any requested draft status. Opening a PR does not authorize merging it or starting persistent monitoring. Continue outstanding implementation work before entering a separate Babysit pass.

Reply with the PR URL, resulting behavior, verification, and material unresolved limitations.
