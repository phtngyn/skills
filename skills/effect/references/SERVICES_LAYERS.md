# Services, Layers, And Modules

## Domain Organization

Group behavior by the domain job, such as `documents/publication.ts` or `media/removal.ts`, rather than collecting unrelated work under mechanism folders such as `services` or `tools`. Split domain internals into independently understandable workflows; a workflow file does not need its own service tag.

Keep the public capability surface small. Introduce a service boundary when callers need an independently useful contract, replaceable dependencies, or separate lifetime ownership. Name adapter ports after the application's job; keep vendor and platform implementations behind those contracts. A `platform` folder is appropriate for adapters, with domain rules staying in their owner.

Compose layers at each host or executable entrypoint, using named subgraphs when the graph grows. Colocate straightforward service implementations; separate large implementations or alternative backends as needed. Choose package boundaries separately from folder layout. These are design defaults, not requirements for one service per file or a particular monorepo structure.

For finite lifecycles, introduce a state machine when legal transitions, modes, or cancellation warrant it; ordinary workflows can remain direct Effects. See [RESOURCES_RUNTIME.md](RESOURCES_RUNTIME.md) for matching construction dependencies to their owner's lifetime.

This organization guidance is informed by [Structure an Effect codebase by domain](https://ratstack.sh/lore/structure-effect-by-domain); its capability projections, cartridges, XState integration, and lint policies are optional house conventions.

## Naming Defaults

| Surface | Default |
| --- | --- |
| Application service file / class | `Database.ts` / `Database` |
| Service identifier | Unique package/path/name, such as `myapp/db/Database` |
| Operation span | `Database.query`, matching the operation |
| Error class / tag | Meaningful failure name, such as `UserNotFound` |
| Layer | `layer`; purpose variants such as `layerConfig`, `layerTest`, `layerMemory` |
| Library module | Named public exports; optional namespace projection in a separate barrel |

These are conventions, not Effect requirements.

## Application Services

Use a domain-named class. A separate interface is useful when shared; otherwise keep the shape beside the tag and derive `Database["Service"]` when needed.

```ts
import { Context, Effect, Layer } from "effect"

export class Database extends Context.Service<Database, {
  readonly query: (sql: string) => Effect.Effect<ReadonlyArray<unknown>>
}>()("myapp/db/Database") {
  static readonly layer = Layer.effect(
    Database,
    Effect.gen(function* () {
      const query = Effect.fn("Database.query")(function* (sql: string) {
        yield* Effect.logDebug("Executing query", { sql })
        const rows: ReadonlyArray<unknown> = []
        return rows
      })
      return Database.of({ query })
    }),
  )
}

export type DatabaseService = Database["Service"]

export const program = Effect.gen(function* () {
  const database = yield* Database
  return yield* database.query("SELECT 1")
})
```

The query is a shape illustration; a real adapter adds typed failures, redaction, parameterized queries, and resource ownership.

Static layers colocate a straightforward implementation with its service. Separate adapters and exported layer functions are appropriate when implementation dependencies or multiple backends warrant them. Keep data/effect/stream-valued members when they express the contract; zero-argument methods are also appropriate. A service class is a tag, not a mutable application object.

## Library Modules And Exports

Upstream library modules often expose a same-name interface and service value. A barrel projects the module as a namespace:

```ts
// index.ts: project a separate leaf module.
export * as Database from "./Database.js"
```

Sibling implementations import the owning leaf directly, avoiding their own aggregate barrel. Consumers of other packages use public exports. Keep local codecs, helpers, and implementation details private.

Domain-named application classes and namespaced library modules are different surfaces. Generic `Interface` / `Service` names and cyclic leaf self-exports may be retained as an explicit existing project convention, but are not the upstream application default.

Use ES modules for runtime organization. Type-only companion namespaces can describe associated types; library type IDs, prototypes, `dual` overloads, and generic casts are not application-service templates.

## Layer Constructors And Names

| Constructor | Produced value |
| --- | --- |
| `Layer.succeed(Tag, impl)` | Already-built implementation |
| `Layer.sync(Tag, () => impl)` | Lazily constructed synchronous implementation |
| `Layer.effect(Tag, acquisition)` | Effectfully acquired implementation |
| `Layer.effectContext(acquisition)` | Multiple intentional service outputs |
| `Layer.unwrap(effect)` | Layer chosen through config or runtime discovery |
| `Layer.effectDiscard(effect)` | Initialization/background work without a service output |

Choose the constructor matching acquisition; a simple implementation need not use a generator.

| Name | Contract |
| --- | --- |
| `layer` | Primary implementation or composition; requirements remain visible in its type |
| `layerNoDeps` | Upstream application convention for an implementation whose dependencies have **not been provided**; it can still require services |
| `layerConfig` | Configuration-backed factory, often accepting `Config.Wrap<Options>` |
| `layerMemory`, `layerTest` | Purpose-specific implementation or test composition |
| `layerWithSqlClient` | Composition intentionally exposing an additional dependency |
| `make`, `layerFrom` | Library constructor / layer built from an acquisition, when needed |

Add variants only when callers need them. The type, not the name, determines outputs, errors, and requirements.

- `Layer.provide` satisfies requirements and hides provided dependencies from output.
- `Layer.provideMerge` also exposes the dependency for downstream consumers.
- `Layer.mergeAll` combines independent exposed layers.
- Name meaningful subgraphs and make required authority explicit.
- Use `Context.Reference` for genuinely defaultable ambient settings or feature flags. Required credentials, persistence, or transports belong in explicit service contracts.

See [RESOURCES_RUNTIME.md](RESOURCES_RUNTIME.md) for sharing, fresh acquisition, finalizers, and runtime ownership.

## Reusable Effect Functions

Use named `Effect.fn` for useful operation spans; prefer `fnUntraced` for library functions and hot paths without useful tracing. Plain pure functions remain plain functions. Avoid reusable functions whose only purpose is returning a new `Effect.gen` when an Effect function expresses the same workflow.

Whole-call transforms belong in extra `Effect.fn` arguments. They receive the effect and original arguments; apply combinators to that effect rather than piping the function itself.

```ts
import { Effect } from "effect"

export const readAttachment = Effect.fn("Attachment.read")(
  function* (id: string) {
    return yield* Effect.succeed({ id })
  },
  (effect, id) => effect.pipe(Effect.annotateLogs({ attachmentId: id })),
)
```

Use transforms for whole-call mapping, errors, logs, deadlines, cleanup, or provisioning. Keep branch-specific recovery in the workflow. Use `Effect.fn.Return<A, E, R>` when an explicit generator contract helps inference or review.

For error translation and shared helpers, read [ERRORS.md](ERRORS.md).

## Source Anchors

At the source revision named in `SKILL.md`: `ai-docs/src/01_effect/03_services/01_service.ts`, `20_layer-composition.ts`, `ai-docs/src/01_effect/01_basics/02_effect-fn.ts`, and `packages/effect/src/http/index.ts`. These demonstrate application tags, layer variants, tracing selection, and separate barrel namespaces.
