---
name: effect
description: Design, implement, refactor, and review Effect code using the latest stable release. Use for composition, typed errors, schemas, services and layers, resource ownership, concurrency, integrations, testing, and reusable APIs.
---

# Effect

Use the latest published stable Effect release. Verify the registry's `latest` version once at the start of implementation or migration, align companion packages with their compatibility requirements, and update the project's dependency declarations and lockfile when needed. Make the upgrade and its affected behavior visible in the work. Use the project's `repo/effect` (or `repos/effect`) clone and resolved declarations matching that release; an unreleased checkout can have different behavior despite the same package version.

Choose the smallest design that satisfies the caller. A finite program can compose Effects directly. A service exposes a useful replaceable capability, a Layer constructs it, and a Scope owns resources. Introduce each boundary for a concrete dependency, substitution or lifetime requirement.

## Work From The Contract

1. Trace inputs, results, expected failures, dependencies and resource owners. For a bug or review, include failure, interruption and cleanup paths.
2. Keep pure decisions as functions. Preserve the success, error and requirement types of composed operations. Capture stable dependencies at construction; leave invocation-specific context with the caller.
3. Keep side effects lazy and compose them until the execution boundary. Decode foreign input and translate failure where representations or responsibilities change.
4. Verify the changed caller contract and simplify within scope. Preserve project conventions and public contracts; refactor for a demonstrated correctness or complexity problem.

A fiber needs a lifetime and a failure policy. Shared mutable state needs an owner and coordination across suspension points. Concurrent requests need a deliberate policy: join, queue, replace or coalesce. Retry requires a transient failure and a safe repeated operation.

## Read Only The Relevant Guide

- [Architecture](references/ARCHITECTURE.md): service boundaries, dependency capture and Layer composition.
- [Boundaries](references/BOUNDARIES.md): schemas, errors, foreign adapters and configuration.
- [Lifetimes](references/LIFETIMES.md): acquisition, sharing, runtime ownership and shutdown.
- [Concurrency](references/CONCURRENCY.md): fibers, state transitions, readiness and streams.
- [Operations](references/OPERATIONS.md): retry, deadlines, caching, batching and persistence.
- [Testing](references/TESTING.md): fakes, controlled races, virtual time and compiler checks.
- [Libraries](references/LIBRARIES.md): consumer APIs, inference and reusable abstractions.
- [Source lookup](references/SOURCE.md): uncertain APIs, platform features or release-specific behavior.

Small edits need only the guides relevant to their changed behavior. Reuse verified API evidence during the task; investigate again when a new requirement, failure or contradictory result warrants it.
