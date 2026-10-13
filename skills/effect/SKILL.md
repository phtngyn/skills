---
name: effect
description: Design, implement, refactor, and review Effect v4 applications and libraries. Use for service boundaries, layer composition, schemas and typed errors, resource lifetimes, concurrent workflows, runtime integration, and testing.
---

# Effect

Build around domain capabilities and explicit ownership. An Effect describes work, a service exposes a capability, and a Layer constructs the implementation. A Scope owns resources and background work. Make those boundaries agree.

Applications are the default. Use the library branch for reusable public APIs. When used with `build`, this skill supplies Effect design and implementation decisions.

## Working Approach

1. **Trace the behavior.** Follow one concrete workflow from input through state changes to output. Identify the expected failures, dependencies, and owner of any resource or background work. For a review or bug, trace the competing paths through failure, cancellation, and shutdown too.
2. **Choose the boundaries.** Keep pure decisions as functions. Put replaceable capabilities and owned state behind services. Compose implementations with Layers at the application boundary. For new architecture, explain the important ownership and failure choices briefly; for an ordinary edit, work within the established design.
3. **Implement a complete slice.** Decode at entry, perform the workflow, and translate its result at the exit. Keep execution in the process or framework host. Use [source lookup](references/SOURCE.md) to settle an unfamiliar API or uncertain semantics, then reuse that evidence.
4. **Prove and simplify.** Check observable behavior, including the lifecycle or concurrency contract changed by the task. Remove redundant wrappers, service tags, error translations, and legacy paths within scope. Report the outcome and actual checks.

## Design Defaults

- **Services represent capabilities.** Introduce a tag for a useful caller contract, replaceable dependency, or lifetime owner. A function or file does not automatically need a service.
- **Dependencies follow lifetimes.** Capture stable dependencies when constructing a service. Supply request context and borrow keyed resources when the operation needs them. A long-lived service must not retain a shorter-lived resource beyond its owner.
- **Effects compose until the edge.** Use `Effect.gen` for inline workflows and named `Effect.fn` for meaningful operations. Run them through the application's host, not from inside domain services.
- **Failure is part of the contract.** Typed errors describe expected failure; defects describe broken assumptions; interruption describes cancellation. Recover where the caller can make a truthful decision.
- **State has one owner.** Keep mutable implementation state private. Coordinate transitions that cross suspension points. Define which concurrent requests join, queue, replace, or coalesce.
- **Resources have a closing path.** Acquire resources and start background work in the scope that owns them. A fiber needs a failure policy as well as a lifetime.
- **Validation belongs at trust boundaries.** Decode foreign representations once, pass trusted domain values inward, and encode at the outward boundary.
- **Use the existing mechanism.** Prefer Effect's resource, concurrency, scheduling, caching, and platform tools when their semantics fit. Add application machinery for a demonstrated contract that they do not supply.

## Guides

For a new application capability or Promise-facing host, read Architecture and Boundaries before implementation; supplied consumer types do not settle construction, ownership, or error policy. Then read the guides for the remaining decisions. A small edit to an established design need not load all of them.

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

For an application architecture study, [OpenCode v2](references/OPENCODE.md) provides implementation and regression evidence. [Provenance](PROVENANCE.md) distinguishes source facts from these personal design defaults.
