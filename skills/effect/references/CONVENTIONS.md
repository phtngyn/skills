# Naming, Structure, And Style

These defaults are extracted from Effect's application examples, public modules, and repository tooling. Follow established consuming-project conventions. Source-repository choices such as import extensions and formatting depend on that repository's toolchain.

## Names Communicate Contracts

| Surface | Default and meaning | Canonical evidence |
| --- | --- | --- |
| Application service | Domain-named class/file such as `Database` / `Database.ts`; the tag represents a capability | `ai-docs/src/01_effect/03_services/01_service.ts` |
| Service identifier | Unique package/path/name such as `myapp/db/Database`; distinguish independently provided tags | Same service example |
| Operation span | `Database.query`, matching a useful operation boundary | `ai-docs/src/01_effect/01_basics/02_effect-fn.ts` |
| Layer | `layer` for primary implementation, purpose variants only when needed; detailed contracts in [SERVICES_LAYERS.md](SERVICES_LAYERS.md#layer-constructors-and-names) | `ai-docs/src/01_effect/03_services/20_layer-composition.ts` |
| Failure | Meaningful error/reason names such as `UserNotFound`; tags distinguish recoverable cases | `ai-docs/src/01_effect/04_errors/20_reason-errors.ts` |
| Library module | Concept name such as `Ref`; functions describe operations such as `make`, `get`, `modify` | `packages/effect/src/Ref.ts` |
| Constructors and conversions | `make`, `from…`, `to…` express different creation/conversion jobs; inspect the actual return contract | `Ref.ts`, `DateTime.ts` |
| Guard | `is…` narrows a public type or variant | `Request.ts` (`isRequest`), `Option.ts` |
| Effectful counterpart | Names such as `mapEffect` distinguish an effectful callback from a pure transformation | `Stream.ts` |
| Unsafe counterpart | Names such as `makeUnsafe` expose a guarantee the caller must own; inspect whether it concerns execution, validation, or lifetime | `Ref.ts`, `DateTime.ts` |

Keep names close to the domain and observable operation. A convention is a useful signal, not a substitute for the signature. In particular, `layerNoDeps` in upstream application examples means dependencies have not been provided; its type can still require services.

## Application Shape

Use upstream fixtures to study complete boundaries, not just isolated tags. `ai-docs/src/51_http-server/fixtures` separates domain contracts, API declarations, service implementations, and HTTP handlers. `server/Users.ts` keeps SQL work behind the `Users` service; `server/Users/http.ts` wires handlers to that capability. Entry/composition layers decide which implementation is available.

Choose a layout that makes ownership and callers easy to follow. For the personal domain-oriented organization preference, read [SERVICES_LAYERS.md](SERVICES_LAYERS.md#domain-organization). A file, folder, service tag, and package are separate boundaries; create each for an actual contract or ownership need.

## Imports And Exports

- Application examples use supported public imports, including named modules from `effect` and domain entrypoints. Preserve the project's import convention and check actual exports.
- Effect's library implementation imports owning leaf modules directly, commonly as namespaces, and keeps runtime imports distinct from type-only imports. This keeps dependencies explicit and avoids importing its own aggregate barrel.
- Public barrels may project leaf modules as namespaces. Keep implementation helpers private; publish a symbol because consumers need its contract.
- The extraction checkout uses relative `.ts` extensions. Consumers must follow their own TypeScript/runtime configuration; examples with `.js` extensions are not a universal Effect rule.
- Generated `@barrel` sections belong to their generator. Apply the target repository's generation procedure when changing that surface.

Canonical sources: `packages/effect/src/Ref.ts`, `packages/effect/src/http/index.ts`, `packages/tools/oxc/oxlintrc.json`, and `.oxlintrc.json`. The source lint rules exempt tests and examples from some implementation import restrictions; preserve that distinction.

## Code Style

Use `Effect.gen` for inline sequential workflows and `Effect.fn` / `fnUntraced` for reusable Effect functions according to [SERVICES_LAYERS.md](SERVICES_LAYERS.md#reusable-effect-functions). Pure computation can remain a plain function. Keep branch logic in the workflow and apply whole-operation policy through combinators.

Define public capability types explicitly where they communicate a stable contract; allow useful local inference. Readonly fields communicate model ownership, while mutable implementation state stays with its owner. Neither inferred exports nor mutable containers are universally forbidden by upstream.

Let the project's formatter and lint configuration establish mechanical style. For new code intentionally adopting Effect's repository style, its `dprint.json` uses two-space indentation, double quotes, ASI, no trailing commas, and a 120-column width; its shared lint config prefers generic array syntax such as `Array<A>`. Adopting that style does not require replacing an existing application's tooling.

Write comments that explain non-obvious intent or invariants. Upstream teaching examples contain explanatory comments intended for documentation; production code should retain only comments useful to its maintainer. Public library documentation follows [LIBRARY_DESIGN.md](LIBRARY_DESIGN.md#documentation-and-validation).

Paths refer to the extraction checkout recorded in [PROVENANCE.md](../PROVENANCE.md); verify current conventions through the [source workflow](SOURCE_WORKFLOW.md).
