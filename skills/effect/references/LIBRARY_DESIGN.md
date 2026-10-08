# Reusable Library Design

Read this branch when designing a public reusable module or changing consumer inference. Application services use [SERVICES_LAYERS.md](SERVICES_LAYERS.md). Study a nearby module of the same kind in the matching source before choosing library machinery.

## Start With Consumer Expressions

Sketch the useful imports, constructor calls, direct calls, and compositions consumers need. Establish what they infer, which failures they can recover from, and which requirements remain. Add abstraction only when it improves those expressions or preserves a real invariant.

Public Effect modules commonly separate a model type, constructors, guards, operations, and associated utility types. Their documentation groups those concepts for discovery. A module can export an interface and functions directly; a separate barrel can project it as a namespace. Related types can live in a type-only companion namespace. Follow the closest comparable public module instead of reproducing every convention in every library.

Canonical comparisons: `packages/effect/src/Ref.ts` for a small state handle, `Request.ts` for associated success/error/requirement types, and `http/HttpClient.ts` for a service-backed module.

## Combinators And Inference

Offer data-first and data-last forms when both direct invocation and piped composition are useful public contracts. Inspect `Function.ts` (`dual`) and the owning module's overloads. Arity dispatch, optional arguments, and overload resolution are runtime/type contracts; verify both call forms rather than mechanically wrapping every function in `dual`.

Keep pure callbacks distinct from effectful callbacks where the distinction matters, as in `map` and `mapEffect`. Preserve the success, error, and service requirements contributed by callbacks. Selected generic signatures should infer useful consumer types and retain intentional narrowing rather than widening everything for implementation convenience.

Choose variance from what the public model consumes and produces. For example, a mutable `Ref<A>` is invariant; a producer and consumer need different analysis. Inspect the model's variance markers and related type tests when changing this contract. Use `NoInfer` or similar utilities for a demonstrated inference constraint, supported by a consumer expression that fails before the fix.

An implementation cast can bridge a proven internal representation, but it cannot prove the public generic contract. Keep such casts local, explain the invariant when unclear, and test the affected consumer behavior. Application code should use public constructors and validated boundaries.

## Representations And Ownership

Type IDs, prototypes, `Pipeable`, inspection, equality, and hashing are useful when the public abstraction needs their semantics or must participate in those protocols. Inspect an analogous module and its tests before implementing one. A service wrapper or plain domain record rarely needs all of them.

Expose resource acquisition through Effects/layers whose requirements and scope communicate ownership. Keep unsafe constructors visibly distinct and document the guarantee the caller assumes. Capture dependencies at acquisition when they belong to the handle's owner; preserve call-time requirements when callers intentionally provide them. Read [RESOURCES_RUNTIME.md](RESOURCES_RUNTIME.md) for sharing and disposal.

Options should express actual consumer policy. Introduce purpose-specific constructors or layers when they simplify a real use case. Keep internal helper shapes private so consumers do not become coupled to an implementation detail.

## Documentation And Validation

Document what consumers can rely on, when to choose the API, and verified gotchas. Examples should demonstrate useful composition or non-obvious behavior. Inspect neighboring public declarations for categories, stability, and version tags.

Within Effect itself, read `.agents/skills/jsdocs/SKILL.md` and its relevant branches. Its public JSDoc, runnable examples, and generated barrels have repository-specific validation. For another library, use that project's documentation and packaging checks; these tags and commands are optional conventions until adopted there.

Validate by the contract changed:

- **Executed behavior:** focused runtime coverage for direct and piped forms, failure, cleanup, and other relevant semantics.
- **Compiler behavior:** focused type tests for intended inference, assignability, rejection, narrowing, overload selection, or displayed public types.
- **Ordinary declarations:** the consuming project's type-check; an exported function alone does not justify a separate type-test suite.
- **Published surface:** when package exports or build output changes, verify the consumer import against the built/packed surface using the project's existing checks.

For a regression, establish that the relevant assertion fails against the original behavior/type. See [TESTING.md](TESTING.md) for runtime and compiler branches.

Canonical extraction sources: `Ref.ts`, `Request.ts`, `Function.ts`, `http/HttpClient.ts`, their focused `test`/`typetest` files, `.agents/skills/test-development`, and `.agents/skills/jsdocs`. See [provenance](../PROVENANCE.md).
