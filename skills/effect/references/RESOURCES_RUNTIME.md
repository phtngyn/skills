# Resources And Runtime Boundaries

## Scope Owns Lifetime

Use `Effect.acquireRelease` when acquisition creates a resource that must be released even after failure or interruption. Its acquisition and release are protected from interruption; make blocking acquisition cancellation decisions deliberately. Use `Effect.acquireUseRelease` for one acquire/use/release operation and `Effect.scoped` at the boundary that closes an explicit scope.

```ts
import { Context, Effect, Layer } from "effect"

export class Connection extends Context.Service<Connection, {
  readonly query: (sql: string) => Effect.Effect<string>
}>()("myapp/Connection") {
  static readonly layer = Layer.effect(
    Connection,
    Effect.gen(function* () {
      const resource = yield* Effect.acquireRelease(
        Effect.sync(() => ({ closed: false })),
        (resource) => Effect.sync(() => { resource.closed = true }),
      )
      return Connection.of({
        query: Effect.fn("Connection.query")((sql: string) =>
          Effect.sync(() => {
            if (resource.closed) throw new Error("Connection already closed")
            return sql
          }),
        ),
      })
    }),
  )
}
```

This models lifetime, not a real database client. SDK adapters must represent expected acquisition/use failures honestly and register their actual close operation. Use `Effect.addFinalizer` when cleanup belongs to an already-acquired scope. Reserve `Effect.ensuring` for cleanup attached to an operation; its lifetime differs from a service layer's lifetime.

Layer acquisition must complete. Choose background fiber ownership and supervision using [CONCURRENCY_STATE.md](CONCURRENCY_STATE.md).

## Layer Sharing

Layer memoization shares the same layer value within the relevant memo map and scope. Reuse named layer values for shared resources. Repeated calls to a layer factory can create different identities; identical options do not guarantee sharing.

Keep effect execution and client acquisition out of individual business calls when the resource belongs to the application. Repeated per-call `Effect.provide(clientLayer(...))` can reacquire it. Prefer yielding an acquired client dependency; use `Layer.build` only when explicit construction is needed, inside an owning scope.

Use `Layer.fresh` or local provisioning only when isolation is required. For result and resource caches, read [CACHING.md](CACHING.md).

## Framework And Process Boundaries

For frameworks that own Promise handlers, use a long-lived `ManagedRuntime` to run service workflows. Create it at the application owner, reuse it across handlers, and dispose it when that owner shuts down. Propagate the request's abort signal when the framework supplies one. Translate typed failures before crossing into a Promise response contract.

```ts
import { Effect, ManagedRuntime } from "effect"
import { Connection } from "./Connection.js"

export const runtime = ManagedRuntime.make(Connection.layer)

export const query = (sql: string, signal?: AbortSignal) =>
  runtime.runPromise(
    Connection.use((connection) => connection.query(sql)),
    { signal },
  )

export const shutdown = () => runtime.dispose()
```

Creating a runtime per request forfeits application sharing. Separate runtimes need an intentionally shared memo map if they must share layer acquisition. Avoid a global runtime when the actual owner is a request, account, test, or hot-reloaded host; scope it to that owner and await disposal.

Use the installed platform's `runMain` for process entrypoints and `Layer.launch` for layer-owned applications. Keep `runPromise`, `runSync`, and runtime execution out of service composition; yield or compose effects there.

## Dynamic Service Layers

Use `LayerMap` when a key such as tenant ID chooses a reusable scoped service graph. Define the lookup layer, idle lifetime, and invalidation policy; inspect `LayerMap.Service` and `LayerMap.make` in the installed version. It is not a general replacement for every result cache. Include credentials/config in the ownership and key design so unrelated accounts cannot share resources accidentally.

## Source Anchors

At the source revision named in `SKILL.md`: `ai-docs/src/01_effect/05_resources/10_acquire-release.ts`, `20_layer-side-effects.ts`, `30_layer-map.ts`, `ai-docs/src/04_integration/10_managed-runtime.ts`, and `packages/effect/src/Layer.ts` (`MemoMap`, `fresh`).
