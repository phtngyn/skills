# Concurrency

## Work Ownership

Choose lifetime, failure, and competition policy before starting concurrent work.

| Work | Starting mechanism |
| --- | --- |
| Independent finite operations | `all` / `forEach` with a deliberate concurrency bound |
| Child of the calling fiber | `forkChild`, with its result accounted for |
| Work owned by a Layer or subscriber Scope | `forkScoped`; `forkIn` for an explicitly captured owner |
| Dynamic set of fibers | `FiberSet` |
| Keyed fibers with replacement policy | `FiberMap` |
| Independently owned detached work | `forkDetach` with explicit lifetime and reporting |

Forking gives work a lifetime but does not guarantee a later failure reaches its caller. Join, report, or supervise according to the contract. Prefer typed recovery for operational failures. Cause-level supervisors must make interruption policy explicit; read [Boundaries](BOUNDARIES.md#errors-callers-can-act-on).

Choose whether one item failure should fail a parallel group or be handled around that item. Bound work according to the scarce resource and ordering requirement. Keep layer construction finite even when a consumer runs forever in its scope.

Evidence: [Effect fibers](../../../repos/effect/packages/effect/src/Effect.ts), [FiberSet](../../../repos/effect/packages/effect/src/FiberSet.ts), [FiberMap](../../../repos/effect/packages/effect/src/FiberMap.ts).

## State Transitions

| Primitive | Contract |
| --- | --- |
| `Ref` | Atomic synchronous update/modify of one state value |
| `SynchronizedRef` | Serialized effectful modifications of one value |
| `Semaphore` | Bound or serialize access to a resource/critical section |
| `Deferred` | One completion or readiness result |
| `Latch` | Reusable open/close gate |
| `Queue` | Work distribution, one consumer per item |
| `PubSub` | Broadcast to subscribers |
| `SubscriptionRef` | Current value plus changes |

A synchronous closure-owned Map can be enough when the complete transition happens without suspension. When a transition reads state, suspends, and then writes based on that read, coordinate it explicitly. Separate `Ref.get` / `set` are not an atomic read-modify-write. Atomic replacement of a pointer does not serialize mutation of its object.

Keep critical sections focused on the transition they protect. An effectful lock can hold across I/O, but waiting inside it for work that needs the same lock creates a deadlock. Return cleanup work or notifications from the protected transition and execute them outside when the invariant permits. A mutex does not establish database transaction guarantees.

Evidence: [Ref](../../../repos/effect/packages/effect/src/Ref.ts), [SynchronizedRef](../../../repos/effect/packages/effect/src/SynchronizedRef.ts), [OpenCode keyed mutex](../../../repos/opencode/packages/core/src/effect/keyed-mutex.ts).

## Choose The Same-Key Policy

| Behavior | Design |
| --- | --- |
| Replace active work | `FiberMap` replacement; cancellation is observable behavior |
| Keep active work and ignore another start | `FiberMap` with its only-if-missing policy |
| Join the same computation | Shared pending result with explicit result/eviction lifetime |
| Run every item in order, keys independently | Keyed queue/lock or grouped Stream consumption |
| Run once more with the newest state after active work | Coalescing state machine or serialized sliding-queue consumer |

These policies are different. A fiber registry is not a queue, and a lock that executes every request does not coalesce them. For grouped streams, consume groups and bound their cardinality, buffers, idle lifetime, and concurrent processing so an unconsumed group cannot stall the source.

For reloads that recompute current state, one capacity-one sliding queue and one sequential consumer can retain the newest pending request while active work finishes. Subscribe producers before initial activation. Debounce controls bursts; serialization controls overlap. Commands that must all execute need retention of every command instead.

Readiness must describe the work accepted so far. Track accepted/settled generations when new changes can arrive during activation. Check generation identity before late results update shared state. A wake arriving at the transition to idle must be retained or start a successor. Distinguish stop acknowledgement, one execution's settlement, and waiting until the key is idle even across successors.

Evidence: [Stream.groupByKey](../../../repos/effect/packages/effect/src/Stream.ts), [OpenCode reloads](OPENCODE.md#reload-and-readiness), [session coordinator](../../../repos/opencode/packages/core/src/session/run-coordinator.ts).

## Streams And Backpressure

Expose Streams for event sources and keep producer controls with their owner. Use a Queue for work distribution, PubSub for broadcast, and SubscriptionRef for a current snapshot plus updates. Choose native Effect/platform sources before adapting a foreign async iterable.

Use `map` for pure transformations, `mapEffect` for effectful work, and `runForEach` for a sequential consumer. Choose bounded concurrent transformation only when ordering permits it. Run long-lived consumers in an owned Scope; collect only bounded streams in memory.

Backpressure is the default policy. Add buffering when producer and consumer must decouple, and choose what full capacity means: suspend producers, drop new values, or slide out old values. Unbounded buffers need a bound elsewhere. A live broadcast is not durable delivery; recovery across disconnection needs stored history or another explicit reliability mechanism.

Evidence: [Stream](../../../repos/effect/packages/effect/src/Stream.ts), [PubSub](../../../repos/effect/ai-docs/src/01_effect/07_pubsub/10_pubsub.ts), [OpenCode live versus durable events](../../../repos/opencode/packages/core/src/bus.ts). Verify ordering and shutdown with [Testing](TESTING.md#control-the-interleaving).
