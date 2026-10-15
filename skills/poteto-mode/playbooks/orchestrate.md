### Orchestrate

Run a standing program as a coordinator with an explicit frontier and verifiable units. Read `references/codex.md` first.

1. Define the terminal condition, scope, units, dependency graph, verification gates, and authorization for delivery. Distinguish a long current task from a persistent service. Do not create a scheduler or goal without an explicit request.
2. Store standing orders, a unit board, and the decision trail in one named location. The imported `scripts/orch/orch.ts` helper can maintain local state when Bun is available; inspect its help before use. Otherwise use a local Markdown or TSV board. The helper records state; it never launches agents or keeps a task alive.
3. Compute the ready frontier from completed dependencies. Launch only useful independent units up to the runtime's capacity. Each writer owns a separate worktree or exclusive output. Use sub-coordinators only when they remove real coordination work and the nesting limit permits them.
4. Give each owner a standalone brief with goal, scope, input revision, owned paths, verification, stopping condition, and report format. Record its agent identifier, branch, revision, and expected next artifact. Use fresh agents for independent checks. Serialize integration and stack topology changes under one owner.
5. Drain results at bounded intervals or completion events. Inspect actual diffs, tests, artifacts, and live behavior. Track verdicts against the exact head revision: verified, failed, blocked, or type-check-only. A new head invalidates affected proof. A worker's summary does not replace verification.
6. Diagnose a stall from actual status and missing side effects. Do not launch a replacement writer until the previous writer is stopped or isolated. Consolidate the brief and current evidence before replacement.
7. At phase boundaries, reconcile the unit board with git and PR state, update the frontier, and checkpoint. On restart, re-read the record and verify live processes; do not assume old agent IDs remain active.
8. When all units are verified, perform authorized delivery. Shipping remains a separate gate. On pause, use Pause safely. Report completed, failed, blocked, and unstarted units plus the next frontier.
