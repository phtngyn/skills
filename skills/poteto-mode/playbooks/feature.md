### Feature

**Own the design, implementation, review, and proof.**

1. Trace the affected subsystem.
2. `architect` for the shape.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the **separate-before-serializing-shared-state** principle skill). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Define the scope, file paths, and data shape before implementation. Use a state machine for scattered booleans, a table or registry for branching, or a typed model for repeated shape assumptions, per **principle-model-the-domain**. State the success criteria. When authorized and useful, delegate with the optional `feature, refactoring` role. When multiple implementation shapes are viable, use [$arena](../../arena/SKILL.md) to compare them and keep review independent where possible. Make surgical edits, re-ground upstream-derived files against the source, and verify shared changes through each affected caller.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Rebase into small, ordered commits. Stack follow-ups.
   Use the **sequence-verifiable-units** principle skill, building, verifying, and committing each small unit before the next.
7. If the design is contested, `interrogate` before shipping.
8. If publication is authorized, follow [Opening a PR](opening-a-pr.md).

Keep coupled work with one owner and give that owner the checkpoint. Fan out after the blocking phase across independently verifiable outputs. Update the checkpoint at phase boundaries.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.
