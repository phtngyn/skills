# Testing

## Test The Caller Contract

Choose checks from the behavior changed, not the list of APIs used. Exercise the real workflow with replaceable capabilities and assert observable results. A service declaration normally needs the project's type-check; a public inference or overload requirement also needs a focused consumer type test.

Use `@effect/vitest` with `it.effect` for a new Vitest setup. Retain an established Effect-aware harness in another runner. It should provide test services before constructing Layers that use them, close each test Scope, and surface failed Exits. Use live services only when real time/platform behavior is the subject of the test.

Expected failures, defects, and interruption need different assertions. For resource owners, verify release after success, failure, and interruption. For retries, assert bounded attempts and the final outcome. A bug regression should fail against the original implementation and pass after the change.

For boundary changes, verify rejection before side effects and the promised encoded/decoded representation. For reusable APIs, verify consumer composition and inference. Select only the checks required by the changed contract.

Evidence: [Effect test examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/09_testing), [Vitest integration](/Users/phtngyn/Developer/skills/repos/effect/packages/vitest/src), [OpenCode Bun harness](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/lib/effect.ts).

## Build Useful Fakes

Use `Layer.succeed(Tag, implementation)` for a simple local fake. For a stateful fake used by many tests, expose a separate test-control tag alongside the production tag. The same object can back both; production code depends only on the real capability, while tests inspect records or trigger failures through the control tag.

Replace at the graph composition point so an internally wired production adapter never acquires. Use real domain logic with fake I/O, rather than reproducing the domain algorithm inside a mock. Keep mutable fake state per test unless the suite deliberately shares and resets it.

For offline tests, an HTTP replacement can reject and record unexpected network attempts. Assert the records after execution so application error recovery cannot hide a missing fake. Use provider Layers for config decoding tests and direct configuration services for workflows that only need decoded values.

Evidence: [Layer test composition](/Users/phtngyn/Developer/skills/repos/effect/packages/vitest/src), [OpenCode network guard](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/lib/effect.ts), [composition rules](ARCHITECTURE.md#compose-at-the-owner).

## Control The Interleaving

Use `Deferred`, Queue, or explicit test hooks to establish readiness and release blocked work. Use `TestClock` from `effect/testing` for sleep, retry, TTL, and polling. Fork the waiting work before advancing the clock. Avoid elapsed-time guesses for ordering assertions.

```ts
import { assert, it } from "@effect/vitest"
import { Effect, Fiber } from "effect"
import { TestClock } from "effect/testing"

it.effect("finishes after its delay", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.sleep("1 second").pipe(
      Effect.as("done"),
      Effect.forkScoped,
    )
    yield* TestClock.adjust("1 second")
    assert.strictEqual(yield* Fiber.join(fiber), "done")
  }),
)
```

For a race, block one path, introduce the competing action, release the block, and assert which result owns the state. Select the scenario relevant to the contract:

| Contract | Interleaving to prove |
| --- | --- |
| Retry or deadline | Gate an attempt, advance virtual time, and assert the attempt bound or cancellation outcome |
| Cache or batching | Concurrent callers share the expected lookup/batch while failures and eviction follow the chosen policy |
| Replaceable resource graph | Old boot fails/releases after its replacement becomes available |
| Coalesced refresh | Change arrives during the initial refresh or just before idle |
| Serialized work | Another trigger arrives while the first operation is gated |
| Combined failure | An expected failure coincides with a finalizer or sibling defect; assert the complete failed Exit and that typed recovery does not hide the defect |
| Scoped registrations | One subscriber closes while a healthy peer remains |
| Shutdown settlement | Gate a finalizer and overlap close calls; assert when each caller may finish according to the Scope, runtime or host contract |
| Cancellation | Stop acknowledges while cleanup is gated; settlement waits for the right generation |
| Callback source | Emit as soon as registration is available; gate asynchronous setup separately when readiness is promised |
| Streaming resource | Gate consumer demand or cancellation, then close its owner; assert bounded upstream pulls, cleanup completion and visibility of cancellation defects |
| Durable work | Duplicate admission, execution success followed by settlement failure, or restart before execution |
| Ordered publication | First writer commits but pauses before publication while a second writer proceeds |
| Replay/live stream | Consumer acknowledgement or replay is blocked while the live tail fills; assert bounded retention and upstream cleanup |

Use the [application examples](APPLICATIONS.md#choose-the-relevant-workflow) for concrete regression scenarios. OpenCode v2 covers shared execution, subscriber replacement and host-owned streams. T3 Code covers durable work, publication order and replay/live overflow. Each example distinguishes inspected tests from executed checks; keep the consuming application's requirements and runner authoritative.

## Runtime, Types, And Packaging

Use focused runtime coverage for behavior and cleanup. Use the project's existing type-test harness for inference, assignability, narrowing, rejected calls, or overload selection. Verify direct and piped forms when both are public contracts. Keep implementation casts from substituting for evidence of the consumer type.

If exports or packaging changed, verify consumer imports against the built/packed surface. Follow the consuming project's scripts and runner conventions; contributor commands for the Effect repository apply only when changing Effect itself. Run targeted checks, then any required project checks. Report checks that could not run.

Evidence: [Effect type tests](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/typetest), [Libraries](LIBRARIES.md#verification).
