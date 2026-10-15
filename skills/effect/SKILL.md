---
name: effect
description: Design, implement, refactor, and review Effect v4 code. Use for effect composition, schemas and typed errors, services and layers, resources, concurrency, integrations, testing, and reusable APIs.
---

# Effect

Match the design to the operation and its callers. An Effect describes work; ordinary functions and composed Effects can be enough. A service exposes a useful capability, a Layer constructs its implementation, and a Scope owns resources and background work. Introduce those boundaries where dependencies, substitution or ownership justify them.

Use this skill for small programs, applications, framework integrations and reusable libraries. The consuming project's requirements determine the architecture. When used with `poteto-mode`, this skill supplies Effect design and implementation decisions.

## Working Approach

1. **Trace the behavior.** Follow the operation from input to result. Identify expected failures, dependencies, and any resource or background-work owner. For a review or bug, trace competing paths through failure, cancellation and cleanup too.
2. **Choose the boundaries.** Keep pure decisions as functions. Introduce services where substitution or shared ownership helps, and compose their Layers at the owner. For new architecture, explain the important ownership and failure choices briefly; for an ordinary edit, work within the established design.
3. **Implement the contract.** Compose Effects, validate foreign inputs at their boundary, and translate results where the caller's representation changes. Run effects at the process, framework or consumer boundary that owns execution. Use [source lookup](references/SOURCE.md) to settle an unfamiliar API or uncertain semantics, then reuse that evidence.
4. **Prove and simplify.** Check observable behavior, including the lifecycle or concurrency contract changed by the task. Remove redundant wrappers, service tags, error translations, and legacy paths within scope. Report the outcome and actual checks.

## Design Defaults

- **Services represent capabilities.** Introduce a tag for a useful caller contract, replaceable dependency, or lifetime owner. A function or file does not automatically need a service.
- **Dependencies follow lifetimes.** Capture stable dependencies when constructing a service. Supply request context and borrow keyed resources when the operation needs them. A long-lived service must not retain a shorter-lived resource beyond its owner.
- **Effects compose until the edge.** Use `Effect.gen` for inline workflows and named `Effect.fn` when an operation benefits from tracing. Run Effects at the boundary that owns execution; reusable operations preserve their callers' requirements.
- **Failure is part of the contract.** Typed errors describe expected failure; defects describe broken assumptions; interruption describes cancellation. Recover where the caller can make a truthful decision.
- **State has one owner.** Keep mutable implementation state private. Coordinate transitions that cross suspension points. Define which concurrent requests join, queue, replace, or coalesce.
- **Resources have a closing path.** Acquire resources and start background work in the scope that owns them. A fiber needs a failure policy as well as a lifetime.
- **Validation belongs at trust boundaries.** Decode foreign representations once, pass trusted domain values inward, and encode at the outward boundary.
- **Use the existing mechanism.** Prefer Effect's resource, concurrency, scheduling, caching, and platform tools when their semantics fit. Add application machinery for a demonstrated contract that they do not supply.

## Guides

Load guides for the decisions the task requires. Read Architecture when introducing capabilities or changing construction; Boundaries when handling foreign values or failure contracts; Libraries when designing reusable consumer APIs. Follow the established design for small edits. Domain-specific mechanisms such as HTTP, SQL, CLI, reactive state or durable workflows are indexed in Source lookup.

| Decision | Guide |
| --- | --- |
| Module shape, service contracts, dependency capture, layer composition | [Architecture](references/ARCHITECTURE.md) |
| Schemas, expected errors, transport adapters, configuration | [Boundaries](references/BOUNDARIES.md) |
| Acquisition, sharing, runtimes, keyed graphs, registrations, shutdown | [Lifetimes](references/LIFETIMES.md) |
| Fibers, shared state, streams, keyed work, cancellation and readiness | [Concurrency](references/CONCURRENCY.md) |
| Retry, deadlines, caching, batching, HTTP policy, observability and time | [Operations](references/OPERATIONS.md) |
| Fakes, virtual time, controlled races, runtime and compiler checks | [Testing](references/TESTING.md) |
| Consumer expressions, combinators, inference, public models | [Libraries](references/LIBRARIES.md) |
| Unfamiliar APIs or platform features | [Source lookup](references/SOURCE.md) |

The [OpenCode v2 studies](references/OPENCODE.md) show how a substantial application uses Effect. Learn from the contracts its construction, ownership and failure policies satisfy, then apply the relevant lesson to the current task. [Provenance](PROVENANCE.md) distinguishes observed source behavior from general guidance and personal defaults.
