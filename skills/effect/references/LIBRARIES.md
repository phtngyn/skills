# Libraries

Read this branch for a reusable public module. Application service design is in [Architecture](ARCHITECTURE.md).

## Start With Consumer Expressions

Write the imports, construction, direct calls, and compositions consumers need before designing machinery. Establish inferred success, error, and requirement types, along with absence and ownership. A useful public model may expose constructors, guards, operations, and associated types; include only the pieces consumers need.

Study the closest analogous Effect module: [Ref](../../../repos/effect/packages/effect/src/Ref.ts) for a small state handle, [Request](../../../repos/effect/packages/effect/src/Request.ts) for associated types, or [HttpClient](../../../repos/effect/packages/effect/src/http/HttpClient.ts) for a service-backed API. Name operations by their contracts: `make`, `from...`, `to...`, `is...`, and effectful counterparts such as `mapEffect` have distinct jobs.

Keep implementation helpers private. A namespace barrel can project related exports, but the implementation should depend directly on owning modules. Follow the library's import/export conventions rather than imposing Effect's repository formatting.

## Preserve Composition And Inference

Offer data-first and data-last forms when both direct and piped use are useful. `dual` is one implementation tool; arity dispatch and optional arguments still need deliberate contracts. Preserve callback success, failure, and requirement types. Keep pure callbacks separate from effectful callbacks where consumers benefit from the distinction.

Choose variance from what the abstraction consumes and produces. A mutable state handle requires different analysis from a producer. Use `NoInfer` or another constraint for a demonstrated inference problem, with a consumer expression proving the desired behavior. Avoid broad overloads or erased generics that make a useful contract appear more permissive.

Internal casts may connect a proven runtime representation to the public interface. Keep them local and explain non-obvious invariants. A cast does not prove assignability, narrowing, or inference; verify the consumer expression itself.

Evidence: [Function.dual](../../../repos/effect/packages/effect/src/Function.ts), [Ref types](../../../repos/effect/packages/effect/src/Ref.ts), [Effect type tests](../../../repos/effect/packages/effect/typetest).

## Representations And Ownership

Type IDs, prototypes, Pipeable, inspection, equality, and hashing are protocols to implement when the abstraction needs them. A plain record or service adapter rarely needs the whole set. Inspect an analogous implementation and its tests before adding a protocol.

Expose acquisition through Effects or Layers whose types and Scope describe ownership. Capture dependencies when they belong to the handle; preserve call-time requirements when the caller supplies them. Unsafe constructors should name and document the guarantee assumed by the caller. Options and alternate layers should express useful policies rather than anticipated flexibility.

Document what consumers can rely on, when to choose the API, and verified constraints. Examples should show useful composition or surprising semantics. Stability tags, JSDoc categories, and generated barrels follow the target repository's procedure.

Evidence: [Ref model](../../../repos/effect/packages/effect/src/Ref.ts), [Request model](../../../repos/effect/packages/effect/src/Request.ts), [Lifetimes](LIFETIMES.md).

## Verification

- Runtime: direct and piped behavior, expected failure, resource release, and other changed semantics.
- Compiler: useful inferred types, assignability/rejection, narrowing, and overload selection where part of the requirement.
- Packaging: consumer imports against the published surface when exports/build output changed.

An ordinary declaration change needs type-checking, not automatically a type-test suite. A runtime regression with unchanged types needs runtime coverage. Use [Testing](TESTING.md) and the project's established harness; public documentation examples should compile.
