# Concurrency

## Choose Ownership And Competition

Before forking, choose the work's lifetime, failure policy and competition policy.

| Requirement | Starting mechanism |
| --- | --- |
| Independent finite operations | `all` / `forEach` with deliberate concurrency |
| Child work joined by the caller | `forkChild` and an accounted-for result |
| Work owned by a Scope | `forkScoped` or `forkIn` |
| Dynamic or keyed fiber ownership | `FiberSet` or `FiberMap` |
| Independent detached work | `forkDetach` with explicit supervision and shutdown |

Forking alone does not guarantee a later failure reaches the caller. Join, report or supervise it. Do not submit work after its owner closes or rely on a closed scope to suppress an invalid submission. Keep uninterruptible regions limited to transitions that must settle consistently.

Choose whether one item failure fails a parallel group or is handled per item. Bound concurrency by the scarce resource and ordering contract. Same-key requests may join one computation, queue every command, replace current work, or coalesce a burst into a follow-up. A fiber registry and a mutex do not supply all of these policies.

## Coordinate State Transitions

`Ref` supplies atomic synchronous updates; `SynchronizedRef` serializes effectful changes; a Semaphore limits or serializes access. `Deferred` represents one completion result; a Latch represents a reusable gate.

A closure-owned Map can be enough when its whole transition is synchronous. Reads and writes separated by suspension need coordination; separate `Ref.get` / `set` are not atomic read-modify-write. Return cleanup or notification work from a critical section when it need not hold the lock. Waiting inside a lock for work that needs the same lock deadlocks.

For refreshes that recompute current state, a capacity-one sliding queue and a sequential consumer can preserve the newest pending change. Commands that must all execute need retention of every command. Subscribe before the initial refresh when changes can arrive during it.

Define readiness by the fact it establishes. An identifier or accepted request can precede usable initialization or completed execution. Track generations when accepted work overlaps refresh or replacement, guard late results, and settle relevant waiters on failure or cancellation. Distinguish stop acknowledgement from cleanup settlement.

## Streams And Backpressure

Use a Queue for work distribution, PubSub for broadcast, and SubscriptionRef for current state plus updates. Prefer existing platform sources when their semantics fit.

Pull-based pipelines propagate consumer demand. Push sources need an explicit capacity and overflow policy: suspend cooperative producers, drop, slide, coalesce or disconnect as the contract permits. `Stream.callback` defaults to an unbounded queue; set its buffer options deliberately. Synchronous foreign emitters cannot automatically be slowed by an Effect queue.

Install listeners before promising readiness and release them in the stream's Scope. Check setup timing against the selected release instead of assuming registration precedes the first pull. Use `map` for pure transformation, `mapEffect` for effectful work, and `runForEach` for sequential consumption. Concurrent transformation needs deliberate ordering and capacity.

Collect only bounded streams in memory. A bounded final queue does not bound earlier subscriptions, chunks or in-flight delivery. Consider bytes as well as item count when payload sizes vary. If replay is required, define durable cursors, overlap handling, overflow and cleanup across the replay/live handoff. A live broadcast alone does not supply durable delivery.

Verify meaningful interleavings with [Testing](TESTING.md#control-the-interleaving).
