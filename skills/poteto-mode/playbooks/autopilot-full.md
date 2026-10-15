### Autopilot-full

Use for an explicitly authorized queue carried through merge. If merging was not authorized, use Autopilot-stack or leave reviewed PRs open.

1. Define the queue, per-item completion predicates, dependencies, delivery authority, and stopping condition. Follow Orchestrate for the unit board and Codex runtime mechanics.
2. Give each independent item one owner in an isolated worktree. The owner implements, verifies, opens its authorized PR, and performs bounded Babysit work. Record each code-ready head and every later head.
3. Run independent verification of the real behavior at the code-ready revision. A new behavior or redesign gets renewed coverage; a small correction gets focused re-verification of the new head. Inspect the receipts yourself.
4. Merge only when the exact current head satisfies the project's checks and the independent verdict. Follow Shipping for frontier ordering and authority. Never infer a review verdict from green CI alone.
5. Drain the queue, repair failed units, and checkpoint while the task is active. Persistent monitoring requires the user's explicit request and a supported mechanism. Stop or isolate stale owners before replacing them.
6. Return merged PRs, open items, blocked gates, and the actual queue predicate. Do not call a partially completed queue done.
