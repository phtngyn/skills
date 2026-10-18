# Libraries

## Start With Consumer Expressions

Write the imports, construction, direct calls and compositions consumers need before designing machinery. Establish inferred success, error and requirement types, absence representation and execution ownership.

A useful public model may expose constructors, guards, operations and associated types; include the pieces consumers need. Study an analogous module in the selected Effect release when its contract is unfamiliar. Follow the consuming library's export and formatting conventions.

## Preserve Composition And Inference

Preserve callback success, error and requirement types through combinators. Keep pure and effectful callback contracts distinct where that helps callers. Offer data-first and data-last forms when both are useful; `dual` is an implementation tool, while arity dispatch and optional arguments still need deliberate behavior.

Choose variance from what the abstraction consumes and produces. Use `NoInfer` for a demonstrated inference problem and prove it with the consumer expression. Avoid broad overloads or erased generics that make a contract appear more permissive.

An internal cast can connect a verified representation to a public interface, but cannot prove inference or assignability. Keep casts local and verify the consumer type independently.

## Describe Ownership And Representation

Expose acquisition through Effects or Layers whose types describe dependencies and Scope ownership. Capture dependencies when they belong to the handle; preserve call-time requirements when the caller supplies them. Keep execution caller-owned until a host boundary is actually needed.

Type IDs, prototypes, Pipeable, inspection, equality and hashing are protocols to implement when consumers need them. A plain record or service adapter rarely needs them all. Unsafe constructors should name the guarantee assumed by the caller; options should express useful policies.

Document observable guarantees and surprising semantics. Use [Testing](TESTING.md#runtime-types-and-packaging) for runtime, compiler and packaging checks, and [Architecture](ARCHITECTURE.md) when a replaceable service boundary is justified.
