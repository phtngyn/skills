# Testing

## Test The Caller Contract

Choose checks from the behavior changed. Exercise real domain logic with replaceable external capabilities and assert observable results. A bug regression should fail against the original implementation and pass after the change.

Use `@effect/vitest` with `it.effect` for an Effect-aware Vitest setup, or retain the project's established harness. Provide test services before constructing Layers that use them, close test-owned scopes and surface failed Exits. Use live services when real time or platform behavior is the subject of the check.

For a resource contract, test release after the relevant success, failure and interruption paths. For retry, assert the attempt bound and final outcome. Boundary tests should check rejection before side effects and the promised encoded representation. Select checks that prove the changed contract.

## Build Useful Fakes

`Layer.succeed(Tag, implementation)` supplies a simple fake. For a shared stateful fake, a separate control capability can expose records or failure triggers while production code depends on the real contract. Keep fake state per test unless sharing and reset are deliberate.

Replace at graph composition so an internally wired production adapter never acquires. Do not reproduce the domain algorithm in a mock. For offline tests, record unexpected I/O and assert the record after execution, so application recovery cannot hide a missing replacement.

## Control The Interleaving

Use Deferreds, Queues or explicit hooks to establish readiness and release blocked work. Use `TestClock` for sleep, retry, TTL and polling. Fork waiting work before advancing the clock; avoid elapsed-time guesses for ordering.

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

Choose the race that could violate the promise: a new request during refresh, old cleanup after replacement, cancellation while a finalizer is blocked, or failure during a commit/publication handoff. Assert the externally visible result, ownership and settlement. For mixed failure causes, verify that recovery preserves all evidence the caller needs on the selected release.

## Runtime, Types, And Packaging

Use focused runtime checks for behavior and cleanup. A declaration change generally needs type-checking; add consumer type tests for public inference, assignability, narrowing or overload contracts. Test direct and piped forms when both are public.

When exports or build output change, check consumer imports against the published surface. Compile executable documentation examples. Follow the consuming project's runner and scripts; Effect repository contributor checks apply when contributing to that repository. Report the actual checks and any material limits.
