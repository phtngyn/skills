# Source Lookup

Use this guide for an unfamiliar API, an uncertain operational detail, or a feature beyond the core guides. Look up the concrete question needed to make the implementation decision.

## Look Up The Question

Use the project's package declarations and public exports to establish available APIs. For examples and implementation, prefer a task-specified checkout or a nearby version-matched source, then the [cloned Effect repository](/Users/phtngyn/Developer/skills/repos/effect). Keep reference checkouts read-only. Link cloned source with its absolute filesystem path and a line locator when useful; record revision context in provenance.

Search `LLMS.md` and `ai-docs/src` for the concept or symbol, then inspect the relevant exported declaration. Read implementation and focused tests for cancellation, sharing, failure retention, ordering, and cleanup when a signature does not settle them. Use supported public imports, including domain entrypoints such as `effect/http` and `effect/testing`.

Use application examples to study workflows and composition. Use public modules and type tests to study reusable libraries. OpenCode and T3 Code provide application evidence rather than Effect API authority. When an example fails against the consuming project, resolve the specific mismatch from that package's declarations instead of adding a compatibility layer.

Choose architectural evidence through the [application examples](APPLICATIONS.md). OpenCode v2 covers dynamic service graphs, reloadable registrations, shared execution and embedded hosting. T3 Code covers shared Layers, durable admission, worker recovery, publication ordering and replayable streams. In either example, trace the requirement, Effect mechanism, owner, failure policy and supporting assertion. Apply that relationship to the current task; assess custom infrastructure against its requirements.

For uncertain overloads or semantics, make a small compiling/executable probe in an isolated workspace. Reuse established evidence until a new API, error, or contradictory result requires another lookup. If local sources are missing, use official documentation/source and report gaps that materially limit the result.

## Find The Mechanism

Example directories below are under `ai-docs/src`; root modules live in `packages/effect/src` and other package paths are relative to the checkout. Use the exported symbol and concept as search terms, not a copied signature as a specification.

| Decision | Starting source |
| --- | --- |
| Service and layer construction | `01_effect/03_services`; `Context.ts`, `Layer.ts` |
| Acquisition and host integration | `01_effect/05_resources`, `04_integration`; `Scope.ts`, `ManagedRuntime.ts`, `LayerMap.ts` |
| Coordination and concurrency | `Ref.ts`, `SynchronizedRef.ts`, `Semaphore.ts`, `Deferred.ts`, `FiberMap.ts`, `FiberSet.ts` |
| Events and backpressure | `03_stream`; `Stream.ts`, `Queue.ts`, `PubSub.ts`, `SubscriptionRef.ts` |
| Retry, TTL, batching | `06_schedule`, `05_batching`; `Schedule.ts`, `Cache.ts`, `ScopedCache.ts`, `RequestResolver.ts` |
| SQL and transactions | `40_sql`; `sql/` and the selected driver package |
| HTTP clients and APIs | `50_http-client`, `51_http-server`; `http/`, `http-api/` |
| Typed GraphQL operations, client tests, batching | `52_graphql`; `graphql/`, `packages/tools/graphql-generator` |
| RPC, durable workflow, distributed entities | `rpc/`, `workflow/`, `cluster/`; `80_cluster` |
| Reactive state and framework bindings | `reactivity/`, `packages/atom`; `Atom`, `AtomRuntime` |
| CLI, subprocesses, platform I/O | `70_cli`, `60_child-process`; `cli/`, `process/`, platform adapter packages |
| AI models, tools, chat | `71_ai`; `ai/` and the selected provider package |
| Observability and calendar/time | `08_observability`, `07_datetime`; `Metric.ts`, `Clock.ts`, `DateTime.ts`, `Cron.ts` |
| Tests and public types | `09_testing`; `test/`, `typetest/`, `packages/vitest` |

Check existing scheduling, caching, coordination, and platform mechanisms before building a substitute. Select by the contract: a result cache, resource cache, fiber registry, and durable workflow solve different problems.

When contributing to Effect itself, read its current repository instructions and task-relevant contributor skills for validation, code generation, and package registration. Those commands do not define checks for a consuming application.

Evidence: [LLMS.md](/Users/phtngyn/Developer/skills/repos/effect/LLMS.md), [public export map](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/package.json), [provenance](../PROVENANCE.md).
