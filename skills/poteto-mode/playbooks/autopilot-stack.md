### Autopilot-stack

Build and verify a queue as a linear PR stack that the user will land. This playbook does not merge.

1. Define the queue, its ordering, per-layer contracts, and verification gates. Read `references/codex.md` for agent and publication boundaries.
2. Build each dependent layer on its parent's actual revision. Independent analysis can run in parallel; dependency-sensitive edits wait. Isolate every writer and serialize stack mutations.
3. Verify each layer before advancing. Use the real user surface for behavior changes and record proof against the exact head. Run an independent review when available; missing required proof remains blocked.
4. Open authorized PRs with parent branches as bases. Register every layer with the host when supported. A rebase or fix invalidates affected proof, so recheck the touched layers.
5. Perform bounded Babysit work for the completed stack when the request includes getting it ready. Report STACK-READY only when each layer has current evidence and checks. Preserve the stack for the user to merge. Catch the user up using the [ketchup skill](../../ketchup/SKILL.md), linking the stack root and tip with each layer's verdict and anything parked or excluded.
