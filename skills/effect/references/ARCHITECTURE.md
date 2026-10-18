# Architecture

## Choose A Useful Boundary

Start from the operation and its callers. Pure decisions can remain functions; finite workflows can compose Effects directly. Introduce a service when callers need a replaceable capability or a shared owner for state and resources. Keep transport-specific decoding and encoding at its boundary, and share domain behavior below adapters that need it.

A service interface describes success, expected failures and call-time requirements. Use `Context.Service` with an identifier unique in the application. Keep contract and implementation together when small; split them when dependency direction or alternate implementations justify it. File layout and import style follow the consuming project.

## Capture Dependencies At Their Owner

Acquire stable dependencies when constructing a service. Retain request, tenant, transaction or execution requirements on methods when their callers supply them. A long-lived service must not permanently capture a shorter-lived capability.

```ts
import { Context, Data, Effect, Layer } from "effect"

export class StoreError extends Data.TaggedError("StoreError")<{
  readonly cause: unknown
}> {}

export class Store extends Context.Service<Store, {
  readonly put: (value: string) => Effect.Effect<void, StoreError>
}>()("app/Store") {}

export class Documents extends Context.Service<Documents, {
  readonly publish: (value: string) => Effect.Effect<void, StoreError>
}>()("app/Documents") {
  static readonly layer = Layer.effect(Documents, Effect.gen(function* () {
    const store = yield* Store
    const publish = Effect.fn("Documents.publish")(function* (value: string) {
      yield* store.put(value.trim())
    })
    return Documents.of({ publish })
  }))
}
```

`Documents.layer` requires `Store` during construction; `publish` uses the acquired implementation. Some platform clients read context again during execution, so check the adapter's actual capture behavior before assuming construction-time provision fixes its transport or authority.

## Compose At The Owner

| Layer operation | Purpose |
| --- | --- |
| `succeed` / `sync` | Supply an implementation / construct it lazily without effectful acquisition |
| `effect` | Construct a service effectfully, including scoped acquisition |
| `unwrap` | Choose a Layer after configuration or discovery |
| `effectDiscard` | Own initialization or background work without inventing a service |
| `mergeAll` | Expose independent capabilities together |
| `provide` | Satisfy construction requirements while keeping dependencies private |
| `provideMerge` | Satisfy requirements and expose the dependency outputs too |

Compose at the executable, framework, tenant or test boundary that owns acquisition. Replace dependencies before graph acquisition; an outer provided service cannot override an implementation already supplied internally. Start with ordinary Layers and add graph machinery only for requirements they cannot express clearly. Sharing is covered in [Lifetimes](LIFETIMES.md#sharing-and-keyed-graphs).

## Keep Execution Composable

`Effect.gen` sequences inline workflows. Use `Effect.fn` when a reusable operation benefits from tracing; use `fnUntraced` when tracing adds no value. Keep pure transformations synchronous, and wrap side effects in lazy Effect constructors. Capturing an already-started Promise does not defer or repeat its underlying work.

Run Effects at the process, framework or consumer boundary that owns execution. Reusable operations retain their callers' requirements. Named functions, combinators and explicit options are often sufficient; see [Libraries](LIBRARIES.md) for public APIs.
