---
name: effect
description: |
  Build and review Effect v4 applications with source-backed module structure, naming, services, schemas, errors, resource lifetimes, concurrency, and runtime integration. Use for Effect implementation and API selection, including configuration, scheduling, caching, streams, HTTP, and tests.
license: MIT
---

# Effect

Build focused services with explicit contracts and owned lifetimes. Follow established project conventions; these defaults guide new code.

## Source Precedence

This skill uses Effect 4.0.1 source at commit
[`b1d200c40`](https://github.com/Effect-TS/effect/tree/b1d200c40a1dad69def51ebdbf0a1a612a12b8ac)
for structure and API evidence. Selected examples are checked against 4.0.1; this is not an exhaustive API audit.

1. Read the nearest `AGENTS.md` and project-local Effect practices.
2. Inspect the consuming package's installed version, exports, and relevant source signatures.
3. Find the matching read-only local Effect clone, if available. Search its `LLMS.md` and `ai-docs/src` for application examples, then nearby source and tests. A clone may differ from the installed version.
4. Use current upstream primary sources when local evidence is insufficient.

Application examples guide application structure; library internals explain API behavior. Preserve that distinction. Read [V4_APIS.md](references/V4_APIS.md) for migration and import checkpoints.

## Read The Matching Branches

Read all branches materially involved before editing; keep unrelated references unloaded.

| Task | Reference |
| --- | --- |
| Domain organization, module surfaces, naming, services, layers, `Effect.fn` | [SERVICES_LAYERS.md](references/SERVICES_LAYERS.md) |
| Records, brands, variants, optionality, decoding | [SCHEMA.md](references/SCHEMA.md) |
| Error design, translation, recovery, defects, interruption | [ERRORS.md](references/ERRORS.md) |
| Acquisition, finalization, layer sharing, runtime bridges, dynamic services | [RESOURCES_RUNTIME.md](references/RESOURCES_RUNTIME.md) |
| Parallelism, fibers, cancellation, shared state, keyed work | [CONCURRENCY_STATE.md](references/CONCURRENCY_STATE.md) |
| Runtime config, providers, `layerConfig` | [CONFIG.md](references/CONFIG.md) |
| Retry, repeat, polling, backoff, deadlines | [SCHEDULING.md](references/SCHEDULING.md) |
| Memoization, keyed TTL, resource caches, batching | [CACHING.md](references/CACHING.md) |
| Events, pagination, queues, backpressure, stream consumers | [STREAMS.md](references/STREAMS.md) |
| Outgoing HTTP, status handling, rate limits | [HTTP_CLIENTS.md](references/HTTP_CLIENTS.md) |
| Tests, virtual time, fakes, controlled ordering | [TESTING.md](references/TESTING.md) |

## Feature Navigation

Use the installed export map, stability annotations, and matching upstream examples to explore additional features.

| Need | Modules / source search |
| --- | --- |
| SQL and transactions | `effect/sql`, the installed `@effect/sql-*` driver; `SqlClient`, `SqlSchema` |
| Typed HTTP server contracts | `effect/http-api`; `HttpApi`, `HttpApiBuilder` |
| Typed RPC | `effect/rpc`; `Rpc`, `RpcGroup`, `RpcServer` |
| Reactive state and framework bindings | `effect/reactivity`, installed `@effect/atom-*`; `Atom` |
| Durable workflows and distributed entities | `effect/workflow`, `effect/cluster`; `Workflow`, `Entity` |
| Command-line applications | `effect/cli`, platform runtime; `Command` |
| AI integrations | `effect/ai`, installed provider package; `LanguageModel`, `Toolkit` |

A public import path does not imply stability.

## Application Boundaries

- Keep transport handlers thin: decode input, read context, call services, and map failures using [ERRORS.md](references/ERRORS.md).
- Keep network calls outside authoritative database transactions. Decode persisted values when they cannot be trusted.
- Import supported public exports; keep `internal/` private. Avoid unchecked casts that bypass validation or conceal type errors.
