# Architecture

## Start With The Workflow

Organize by the domain job: `documents/publication.ts`, `orders/placement.ts`, or `media/removal.ts`. Keep transport, business decisions, and persistence responsibilities visible, without requiring a separate file or tag for each step. Package boundaries should follow consumers and dependency direction.

A service earns its boundary when it provides a useful capability, owns shared state or resources, or lets callers substitute an implementation. Its interface describes what callers can rely on: success, expected failures, and call-time requirements. A repository, coordinator, provider adapter, or policy engine may earn a tag; a parsing helper usually stays a function.

Choose the smallest boundary that expresses the caller's contract. A finite script can compose one program; an operation can remain an Effect-returning function; a reusable resource can expose scoped acquisition. Use a service and Layer when callers need a replaceable capability or a shared owner. For public consumer APIs, read [Libraries](LIBRARIES.md).

Keep handlers thin: decode, read request context, call the capability, encode the result. Keep domain decisions outside transport types and vendor APIs. Use explicit state machines when legal transitions or modes need enforcement; straightforward workflows can remain sequential Effects.

For an application capability with shared state and background work, a service constructed by a Layer can align construction and ownership. Keep framework or Promise adapters focused on running operations and translating the consumer contract. Choose the execution host from its owner; runtime ownership is covered in [Lifetimes](LIFETIMES.md#runtime-and-stream-boundaries).

## Construct Services Once

Use `Context.Service` with a unique package/path identifier. Put the implementation beside the contract when it is small; separate alternate or substantial adapters. A service tag identifies a capability, while the returned object and its closure own implementation state.

```ts
import { Context, Data, Effect, Layer } from "effect"

export class InvalidTitle extends Data.TaggedError("InvalidTitle")<{}> {}
export class StoreUnavailable extends Data.TaggedError("StoreUnavailable")<{
  readonly cause: unknown
}> {}

export class DocumentStore extends Context.Service<DocumentStore, {
  readonly put: (title: string) => Effect.Effect<void, StoreUnavailable>
}>()("app/documents/DocumentStore") {}

export class Documents extends Context.Service<Documents, {
  readonly publish: (title: string) => Effect.Effect<void, InvalidTitle | StoreUnavailable>
}>()("app/documents/Documents") {
  static readonly layer = Layer.effect(
    Documents,
    Effect.gen(function* () {
      const store = yield* DocumentStore
      const publish = Effect.fn("Documents.publish")(function* (title: string) {
        const normalized = title.trim()
        if (normalized.length === 0) return yield* Effect.fail(new InvalidTitle())
        yield* store.put(normalized)
      })
      return Documents.of({ publish })
    }),
  )
}
```

`Documents.layer` requires `DocumentStore` during construction. The acquired `publish` method uses that implementation without requiring the tag again. Keep dependencies acquired once when they belong to the service's owner. Keep request-specific requirements on the method when the caller should supply them. Derive an implementation type with `Documents["Service"]` when useful; introduce a separate interface only when it improves reuse or readability.

An Effect-valued member expresses repeatable work, a Stream-valued member expresses a source, and a plain value expresses already-acquired data. Do not turn immutable values into zero-argument Effects merely for uniformity.

Evidence: [service construction](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/03_services/01_service.ts), [application integration](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/04_integration/10_managed-runtime.ts).

## Compose At The Owner

| Layer operation | Decision |
| --- | --- |
| `Layer.succeed` / `Layer.sync` | Supply an existing implementation / construct it lazily without effectful acquisition |
| `Layer.effect` | Construct a service effectfully, including scoped resources |
| `Layer.unwrap` | Choose a Layer after reading configuration or discovering a backend |
| `Layer.effectDiscard` | Start owned initialization or background work without inventing a service |
| `Layer.mergeAll` | Expose independent capabilities together |
| `Layer.provide` | Satisfy construction requirements and keep those dependencies private |
| `Layer.provideMerge` | Satisfy requirements while also exposing the dependency outputs |

Compose named subgraphs at executable, host, tenant, or test boundaries. Keep the requirements visible until that boundary can supply the right implementations. The Layer's type establishes its outputs, errors, and requirements; a name such as `layerNoDeps` is only a project convention.

When replacing an adapter, change the wiring that acquires it. Providing a tag around a workflow cannot replace an implementation that its Layer already supplies internally. Tests and embedding hooks should substitute dependencies before graph acquisition and verify the production adapter's side effects never start.

Start with ordinary Layer composition. Add graph machinery only for requirements such as transitive replacement or separate sharing domains that ordinary wiring cannot express clearly. Resource identity and memoization are covered in [Lifetimes](LIFETIMES.md#sharing-and-keyed-graphs). OpenCode v2 supplies [worked evidence](OPENCODE.md#composition-and-replacement) for those larger graph requirements and [dependency capture](OPENCODE_SESSION.md#put-each-owner-at-the-right-boundary).

Evidence: [Layer composition](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/03_services/20_layer-composition.ts), [Layer declarations](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Layer.ts).

## Make Operations Readable

Use `Effect.gen` for inline sequencing and `Effect.fn("Domain.operation")` for reusable operations with useful tracing. Use `fnUntraced` for helpers or hot paths where a span adds no value. Keep pure transformation, option building, and trusted validation synchronous.

Bind services to meaningful local names before calling methods. Use generators for branching and sequencing; use combinators for whole-operation policy such as error translation, annotations, deadlines, or provisioning. Extra `Effect.fn` arguments transform the returned Effect and receive the original arguments; apply policy there when it covers the whole call.

Name capabilities and operations by their domain job. Keep implementation state private and public contracts explicit where callers rely on them. Follow the consuming project's import, formatter, and export conventions. Import public Effect modules; upstream implementation formatting and namespace style are not architectural requirements.

Evidence: [Effect functions](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/01_basics/02_effect-fn.ts). For public combinators rather than application operations, read [Libraries](LIBRARIES.md).
