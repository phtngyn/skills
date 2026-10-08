---
name: effect
description: Build and review Effect v4 applications and reusable libraries. Use for Effect API selection, naming, module design, services, schemas, errors, resource ownership, concurrency, integration, and testing, verified against local source.
---

# Effect

Build focused services with explicit contracts and owned lifetimes. Applications are the default; load library guidance when designing reusable public APIs. Honor whether the user requests explanation, design, review, or edits, along with their checkpoints and the consuming project's conventions. When used with `build`, this skill supplies Effect-specific decisions within that workflow.

## Work From Source

The skill supplies principles, search pointers, and defaults. The installed package and compatible repository source establish API facts. Examples here are starting points, not proof that an API exists in the target version. Extraction revisions and personal choices are recorded in [PROVENANCE.md](PROVENANCE.md).

1. **Locate once.** Read project instructions and resolve the installed Effect version from the consuming package. Prefer a task-specified checkout, then the project's or a nearby ancestor's `repos/effect`, then this collection's `../../repos/effect` resolved from the skill's real directory. Record the checkout revision and compare relevant exports/signatures with the installed package. Equal version strings alone do not establish identical source.
2. **Read narrowly.** For each material Effect API or pattern introduced or changed, search the local `LLMS.md` and `ai-docs/src`, then inspect its exported signature. Read implementation and focused tests when semantics remain uncertain. Application examples guide application structure; public modules and their tests guide library design. Use [SOURCE_WORKFLOW.md](references/SOURCE_WORKFLOW.md) for discovery failures, version mismatches, and unfamiliar features.
3. **Settle the contract.** Identify success, expected failures, requirements, and any resource or fiber owner. Decide cancellation, retry, and sharing semantics where they affect the request. Ordinary edits can use established contracts directly.
4. **Implement and check.** Make a focused change using matching Effect primitives. Use a small compiling or executable probe to settle uncertain API usage. Validate the changed runtime behavior; test compiler behavior when inference, assignability, or rejection is part of the requirement.
5. **Reuse evidence.** Keep source locations, version information, and verified facts in working context. Reopen them for a new concept, changed version, compiler error, or contradictory result. Finish with the outcome, actual checks, and material limitations; link source evidence when it explains a consequential choice.

Inspect each distinct changed API or pattern once; familiar unchanged calls do not need repeated audits. Keep reference checkouts read-only. Use version-matched official sources when local evidence is unavailable, and state any compatibility uncertainty. Repository contributor commands apply to work in that repository; derive application validation from the consuming project's scripts.

## Principles

These names are this skill's synthesis of Effect's examples and implementation. Use them to steer concrete decisions. Linked guides provide detail when a decision needs it.

| Principle | Decision it changes |
| --- | --- |
| [Source before memory](references/SOURCE_WORKFLOW.md) | Verify new or changed API facts against compatible source before relying on remembered APIs or skill examples. |
| [Contracts first](references/SERVICES_LAYERS.md) | Shape success, typed failures, and dependencies around the caller's capability; introduce service boundaries where they earn their ownership. |
| [Compose before running](references/RESOURCES_RUNTIME.md) | Keep workflows as Effects and layers; execute them at the owning process or framework boundary. |
| [Scope owns lifetime](references/RESOURCES_RUNTIME.md) | Acquire, share, and release a resource within its actual application, request, tenant, or test owner. |
| [Cancellation is behavior](references/CONCURRENCY_STATE.md) | Choose fiber ownership, interruption propagation, and failure policy before starting concurrent work. |
| [Decode at boundaries](references/SCHEMA.md) | Validate unknown representations on entry; model trusted internal values according to their domain. |
| [Use the standard library](references/SOURCE_WORKFLOW.md#find-the-existing-mechanism) | Check Effect's existing mechanism and semantics before implementing scheduling, caching, coordination, or platform plumbing. |
| [Prove the contract](references/TESTING.md) | Verify observable behavior and, when relevant, public compiler behavior with focused checks. |

## Read Matching Guidance

Load a guide when its decision arises and reuse it during the task. A matching canonical source example can answer the question directly; reading every parallel guide is unnecessary. Keep unrelated references unloaded.

| Task | Reference |
| --- | --- |
| Naming, imports, exports, formatting, and code style | [CONVENTIONS.md](references/CONVENTIONS.md) |
| Domain organization, application services, layers, `Effect.fn` | [SERVICES_LAYERS.md](references/SERVICES_LAYERS.md) |
| Reusable library modules, combinators, inference, and public documentation | [LIBRARY_DESIGN.md](references/LIBRARY_DESIGN.md) |
| Records, brands, variants, optionality, decoding | [SCHEMA.md](references/SCHEMA.md) |
| Error design, translation, recovery, defects, interruption | [ERRORS.md](references/ERRORS.md) |
| Acquisition, finalization, layer sharing, runtime bridges, dynamic services | [RESOURCES_RUNTIME.md](references/RESOURCES_RUNTIME.md) |
| Parallelism, fibers, cancellation, shared state, keyed work | [CONCURRENCY_STATE.md](references/CONCURRENCY_STATE.md) |
| Runtime config, providers, `layerConfig` | [CONFIG.md](references/CONFIG.md) |
| Retry, repeat, polling, backoff, deadlines | [SCHEDULING.md](references/SCHEDULING.md) |
| Memoization, keyed TTL, resource caches, batching | [CACHING.md](references/CACHING.md) |
| Events, pagination, queues, backpressure, stream consumers | [STREAMS.md](references/STREAMS.md) |
| Outgoing HTTP, status handling, rate limits | [HTTP_CLIENTS.md](references/HTTP_CLIENTS.md) |
| Logging, tracing, metrics, dates, time zones, and testable current time | [OBSERVABILITY_TIME.md](references/OBSERVABILITY_TIME.md) |
| Tests, virtual time, fakes, controlled ordering | [TESTING.md](references/TESTING.md) |
| v3/v4 migration assumptions and import paths | [V4_APIS.md](references/V4_APIS.md) |

For SQL, HTTP servers, RPC, reactive state, workflows, CLI, AI, and other features, use the [source map](references/SOURCE_WORKFLOW.md#find-the-existing-mechanism) and the installed export map. Public importability and API stability are separate facts.

## Application Boundaries

- Keep transport handlers thin: decode input, read context, call services, and map failures using [ERRORS.md](references/ERRORS.md).
- Keep network calls outside authoritative database transactions. Decode persisted values when they cannot be trusted.
- Import supported public exports; keep `internal/` private. Avoid unchecked casts that bypass validation or conceal type errors.
