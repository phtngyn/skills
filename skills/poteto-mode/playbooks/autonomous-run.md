### Autonomous run

1. Define a checkable exit condition and any user-specified budget or stop condition.
2. Read `references/codex.md` relative to the poteto-mode directory. Continue in the current task using available event waits or bounded polling when needed. Use a persistent lifecycle only when explicitly requested and actually supported. Never claim an inactive task is monitoring.
3. Work in small verifiable units. State each hypothesis, make the smallest justified change, check the real artifact, and keep only improvements.
4. Stay within the authorized scope. Resolve incidental blockers needed for the task; record unrelated discoveries as follow-ups. A stalled experiment calls for new evidence or a new hypothesis, not a weaker completion condition.
5. Log decisions through `show-me-your-work`. Checkpoint branch, revision, artifacts, processes, and remaining work at useful boundaries.
6. Stop when the exit condition is met, the user stops work, a stated budget is exhausted, or a real external blocker prevents progress. Report which occurred and the actual predicate state.
