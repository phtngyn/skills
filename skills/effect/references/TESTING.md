# Testing

## Defaults

```ts
import { assert, it } from "@effect/vitest"
import { Effect, Fiber } from "effect"
import { TestClock } from "effect/testing"
```

Use a v4-compatible `@effect/vitest` version. `TestClock` is under
`effect/testing`, not the root `effect` barrel or the old `effect/TestClock` path.

- Use `it.effect` by default.
- Use `it.live` only when real time or live runtime services are the behavior under test.
- Both provide and close a `Scope`; return scoped effects directly from those tests.
- Effect's own tests use `assert` from `@effect/vitest`; retain an established consuming-project assertion style.
- Use test layers and `ConfigProvider` rather than global mutation.
- Use `TestClock.setTime` / `TestClock.adjust` for sleeps, schedules, retries, leases, and timeouts.
- Fork sleeping effects before advancing `TestClock`.
- Assert typed failures, rollback, interruption, finalization, retry bounds, idempotency, concurrency laws, and malformed persistence where relevant.

```ts
it.effect("advances virtual time", () =>
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

```ts
it.effect("finds a user", () =>
  Effect.gen(function* () {
    const users = yield* UserRepo
    const result = yield* users.find(UserId.make("u1"))
    assert.strictEqual(Option.isSome(result), true)
  }).pipe(Effect.provide(UserRepo.layerTest)),
)
```

## Synchronization Instead Of Sleeps

Choose coordination primitives using [CONCURRENCY_STATE.md](CONCURRENCY_STATE.md). Use explicit test hooks when the boundary needs a deterministic readiness point.

```ts
it.effect("publishes exactly once", () =>
  Effect.gen(function* () {
    const published = yield* Queue.unbounded<Message>()
    const ready = yield* Deferred.make<void>()

    const runWorker = makeWorker({
      onReady: () => Deferred.succeed(ready, undefined),
      onPublish: (message) => Queue.offer(published, message),
    })

    yield* runWorker.pipe(
      Effect.forkScoped,
    )

    yield* Deferred.await(ready)
    const message = yield* Queue.take(published)

    assert.deepStrictEqual(message, expectedMessage)
  }),
)
```

## First-Class App Test Stubs

For reusable stateful fakes, expose a separate test-control tag alongside the production tag. Derive the production implementation type from the tag; use a simple `Layer.succeed` when no controls are needed.

```ts
import { Context, Effect, Layer, Option, Ref, Schema } from "effect"

type Message = { readonly text: string }
class SendError extends Schema.TaggedError<SendError>()("SendError", {}) {}

export interface NotifierService {
  readonly send: (message: Message) => Effect.Effect<void, SendError>
}

export class Notifier extends Context.Service<Notifier, NotifierService>()(
  "myapp/Notifier",
) {}

export interface NotifierTestService extends NotifierService {
  readonly sentMessages: () => Effect.Effect<ReadonlyArray<Message>>
  readonly failNextSend: (error: SendError) => Effect.Effect<void>
}

export class NotifierTest extends Context.Service<NotifierTest, NotifierTestService>()(
  "myapp/Notifier/Test",
) {}

export const layerTest = Layer.effectContext(
  Effect.gen(function* () {
    const sent = yield* Ref.make<ReadonlyArray<Message>>([])
    const nextFailure = yield* Ref.make<Option.Option<SendError>>(Option.none())

    const service = NotifierTest.of({
      send: Effect.fn("Notifier.Test.send")(function* (message) {
        const failure = yield* Ref.getAndSet(nextFailure, Option.none())
        if (Option.isSome(failure)) return yield* Effect.fail(failure.value)
        yield* Ref.update(sent, (messages) => [...messages, message])
      }),
      sentMessages: Effect.fn("Notifier.Test.sentMessages")(function* () {
        return yield* Ref.get(sent)
      }),
      failNextSend: Effect.fn("Notifier.Test.failNextSend")(function* (error) {
        yield* Ref.set(nextFailure, Option.some(error))
      }),
    })

    return Context.empty().pipe(
      Context.add(Notifier, service),
      Context.add(NotifierTest, service),
    )
  }),
)
```

Guidance:

- The same object can back both the production `Notifier` tag and test-control `NotifierTest` tag.
- Production code depends only on the real service tag.
- Tests use `NotifierTest` for control and inspection.
- Use `Layer.mock` only for tiny local partial mocks where omitted members should fail loudly if used.

## Config In Tests

Use `ConfigProvider.layer(ConfigProvider.fromUnknown(...))` when the test should exercise Config decoding.

Use `Layer.succeed(AppConfiguration, config)` when the app wraps decoded config in its own service and the test does not need to exercise env decoding.

## Shared Test Layers

`layer(...)` from `@effect/vitest` acquires a shared layer for a test block and tears it down afterward. Mutable service state persists between tests in that block. Use this intentionally for expensive shared resources; use per-test acquisition or reset controls when cases require isolated state. Test acquisition/release and interruption for resource-owning services.

## Compiler Behavior

Use a focused type test when the requirement is TypeScript inferring, accepting, rejecting, narrowing, or selecting an overload for a consumer expression. An exported declaration alone needs the project's type-check, not automatically a type-test suite. A runtime regression with an unchanged type contract needs runtime coverage.

Inspect nearby type tests and use the project's existing harness. In Effect itself, read `.agents/skills/test-development/types.md` and use the relevant `packages/effect/typetest` example. Structural type equality does not establish editor quick-info rendering; displayed-type regressions use the separate `displayed-types.md` branch.

For a regression, confirm the assertion fails against the original implementation/type and passes after the change. Derive targeted non-watch commands and applicable checks from the consuming project's scripts and instructions. Report checks that could not run. For library API design, read [LIBRARY_DESIGN.md](LIBRARY_DESIGN.md).

## Source Anchors

At the revisions in [provenance](../PROVENANCE.md): `ai-docs/src/09_testing`, `.agents/skills/test-development`, `packages/vitest/src`, and the focused runtime/type tests for the changed module.
