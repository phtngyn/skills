---
name: principle-make-operations-idempotent
description: "Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs."
---

# Make Operations Idempotent

Design operations so they converge to the correct state regardless of how many times they run or where the previous run stopped. Every state-mutating operation should answer: "What happens if this runs twice? What happens if the previous run crashed halfway?"

**Why:** Commands, lifecycle operations, and processing loops run where crashes, restarts, and retries are normal. If partial state changes the next run's outcome, every restart becomes a debugging session.

**The idea:** derive each step from the state that exists, not from what the previous run meant to do. Read the current state, compare it to the goal, and apply only the difference. A step written this way is safe to repeat, because a repeat finds nothing left to do.

A later run must be able to distinguish active ownership, completed work and abandoned partial work in artifacts such as locks, temporary files, records and claimed jobs. Judge staleness by evidence that stays true wherever the previous run could have stopped, not only in the common case. A marker that the next run cannot judge turns every crash into manual cleanup. For example, write to a temporary path and rename it into place, or compare artifacts by content instead of by creation order.

**The test:**
1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at every possible point?
3. Does re-execution converge to the same end state?

If partial state makes a repeat duplicate work, corrupt state or remain stuck, add reconciliation or an explicit recovery policy. Some external effects require idempotency keys or reconciliation because local state cannot prove whether they completed.
