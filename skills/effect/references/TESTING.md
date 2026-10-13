# Testing

## Test The Caller Contract

Choose checks from the behavior changed, not the list of APIs used. Exercise the real workflow with replaceable capabilities and assert observable results. A service declaration normally needs the project's type-check; a public inference or overload requirement also needs a focused consumer type test.

Use `@effect/vitest` with `it.effect` for a new Vitest setup. Retain an established Effect-aware harness in another runner. It should provide test services before constructing Layers that use them, close each test Scope, and surface failed Exits. Use live services only when real time/platform behavior is the subject of the test.

Expected failures, defects, and interruption need different assertions. For resource owners, verify release after success, failure, and interruption. For retries, assert bounded attempts and the final outcome. A bug regression should fail against the original implementation and pass after the change.

Evidence: [Effect test examples](../../../repos/effect/ai-docs/src/09_testing), [Vitest integration](../../../repos/effect/packages/vitest/src), [OpenCode Bun harness](../../../repos/opencode/packages/core/test/lib/effect.ts).

## Build Useful Fakes

Use `Layer.succeed(Tag, implementation)` for a simple local fake. For a stateful fake used by many tests, expose a separate test-control tag alongside the production tag. The same object can back both; production code depends only on the real capability, while tests inspect records or trigger failures through the control tag.

Replace at the graph composition point so an internally wired production adapter never acquires. Use real domain logic with fake I/O, rather than reproducing the domain algorithm inside a mock. Keep mutable fake state per test unless the suite deliberately shares and resets it.

For offline tests, an HTTP replacement can reject and record unexpected network attempts. Assert the records after execution so application error recovery cannot hide a missing fake. Use provider Layers for config decoding tests and direct configuration services for workflows that only need decoded values.

Evidence: [Layer test composition](../../../repos/effect/packages/vitest/src), [OpenCode network guard](../../../repos/opencode/packages/core/test/lib/effect.ts), [composition rules](ARCHITECTURE.md#compose-at-the-owner).

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
| Replaceable resource graph | Old boot fails/releases after its replacement becomes available |
| Coalesced reload | Change arrives during initial activation or just before idle |
| Serialized work | Another trigger arrives while the first operation is gated |
| Scoped registrations | One subscriber fails/unloads while a healthy peer remains |
| Cancellation | Stop acknowledges while cleanup is gated; settlement waits for the right generation |
| Streaming host | Close starts while a body/iterator is still being consumed |

OpenCode's [regression tests](OPENCODE.md#regression-tests) supply concrete implementations of several of these scenarios. Tests should prove those contracts, not copy its coordinator or test harness.

## Runtime, Types, And Packaging

Use focused runtime coverage for behavior and cleanup. Use the project's existing type-test harness for inference, assignability, narrowing, rejected calls, or overload selection. Verify direct and piped forms when both are public contracts. Keep implementation casts from substituting for evidence of the consumer type.

If exports or packaging changed, verify consumer imports against the built/packed surface. Follow the consuming project's scripts and runner conventions; contributor commands for the Effect repository apply only when changing Effect itself. Run targeted checks, then any required project checks. Report checks that could not run.

Evidence: [Effect type tests](../../../repos/effect/packages/effect/typetest), [Libraries](LIBRARIES.md#verification).
