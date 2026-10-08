# Concurrency And Shared State

## Choose The Work Policy First

- Independent finite work: `Effect.all` or `Effect.forEach` with an explicit concurrency bound. Decide whether a typed failure should fail the group or be handled per item.
- Child work owned by the calling fiber: `Effect.forkChild`; join or otherwise account for its result.
- Background work owned by a layer/scope: `Effect.forkScoped`; use `forkIn` when a service method must attach work to a captured owner scope.
- A dynamic set of scoped fibers: `FiberSet`; keyed replaceable fibers: `FiberMap`.
- Detached fibers: `forkDetach` only with an explicit independent owner and reporting policy.

A fiber needs both a lifetime owner and a failure policy. Forking does not guarantee that a later failure reaches the caller. Join, supervise, or report failures deliberately. For recovery policy, read [ERRORS.md](ERRORS.md).

Promise adapters should pass the `AbortSignal` supplied by `Effect.tryPromise` to APIs that support it. Callback adapters should return cancellation/finalization logic. Effect interruption cannot cancel an arbitrary foreign Promise unless the underlying API cooperates.

## State And Synchronization

| Primitive | Use |
| --- | --- |
| `Ref` | Atomic synchronous read/update/modify of shared state |
| `SynchronizedRef` | Serialize effectful modifications of one state value |
| `Semaphore` | Bound simultaneous access to a resource or critical region |
| `Deferred` | One-shot completion/readiness result |
| `Latch` | Reusable open/close gate |
| `Queue` | Work handed to one consumer per item |
| `PubSub` | Broadcast to each subscriber |
| `SubscriptionRef` | Current value plus a stream of updates |

Separate `Ref.get` and `Ref.set` are not an atomic read-modify-write. Prefer `update`, `modify`, or `getAndUpdate` when the decision and change must happen together. An atomic pointer update does not make mutations of the referenced object atomic.

```ts
import { Effect, Ref, Semaphore } from "effect"

export const program = Effect.gen(function* () {
  const count = yield* Ref.make(0)
  const permits = yield* Semaphore.make(2)
  yield* Effect.forEach(
    [1, 2, 3],
    () => Ref.update(count, (n) => n + 1).pipe(Semaphore.withPermit(permits)),
    { concurrency: 3, discard: true },
  )
  return yield* Ref.get(count)
})
```

This illustrates primitives; a lone atomic update does not need a semaphore. Use permits around the actual scarce resource or multi-step critical section. Keep critical regions small; locks alone do not establish database transaction guarantees.

## Keyed Work Is Several Different Contracts

| Required behavior | Starting point |
| --- | --- |
| New work cancels/replaces old work for the same key | `FiberMap.run` default replacement policy |
| Keep existing work and reject a new same-key start | `FiberMap.run` with `onlyIfMissing`; verify exact return behavior |
| Process every event in order for each key, keys in parallel | `Stream.groupByKey` and sequential consumption of each group |
| Collapse pending changes into one latest-value rerun after current work | Explicit coalescing state machine or an existing tested helper |
| Serialize callers touching one state/resource | `SynchronizedRef` or a scoped semaphore, depending on the contract |

`FiberMap` owns and replaces fibers; it does not alone queue all events or implement a coalesced rerun. Inspect grouped stream processing before writing custom fiber bookkeeping. Bound key cardinality, buffer sizes, idle lifetime, and concurrent group consumption; leaving emitted groups unconsumed can block the source.

A keyed coalescing helper should specify what happens to active work, pending updates, failures, and disposal. Test late completion after a newer input, independent keys, and shutdown. Reuse a tested helper when its semantics match; do not silently substitute cancellation for ordered processing.

For deterministic ordering, time, interruption, and finalization checks, read [TESTING.md](TESTING.md).

## Source Anchors

At the original API-guide revision in [provenance](../PROVENANCE.md): `packages/effect/src/Effect.ts` (`forEach`, `forkChild`, `forkScoped`, `tryPromise`), `Ref.ts`, `SynchronizedRef.ts`, `Semaphore.ts`, `FiberMap.ts`, and `Stream.ts` (`groupByKey`); corresponding tests own operational behavior.
