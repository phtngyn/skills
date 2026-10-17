# Effect Provenance

This skill teaches design and implementation decisions for Effect v4. Its organization and defaults are our synthesis. Effect source establishes API behavior; OpenCode v2 and T3 Code supply application evidence for construction, ownership, concurrency and delivery guarantees.

## Reviewed Sources

| Source | Reviewed revision | Material used |
| --- | --- | --- |
| [Effect](/Users/phtngyn/Developer/skills/repos/effect) | `742976ce97f5157b00e67e4a5ece6bc04e1899e3` | `LLMS.md`, focused application examples, public declarations/implementation, and test/type-test conventions |
| [OpenCode v2](/Users/phtngyn/Developer/skills/repos/opencode) | `4617210822bdbb31e5749751afbfb4584ccedac8` | Service graph composition, location ownership, plugin registrations, reloads, session coordination, host adapters, and focused regression tests |
| [T3 Code](/Users/phtngyn/Developer/skills/repos/t3-code) | `2fbd4318fc5b610c3e7fcfcbd5bbd80b73521d8f` | Shared Layer wiring, durable command/outbox execution, cancellation registration, commit/publication ordering, bounded replay/live streams and focused regression tests |
| [Writing for Agents](/Users/phtngyn/Developer/skills/repos/mattpocock) | `49dd158d1076134a641b33efb035946536778336` | Decision-oriented hierarchy, conditional context pointers, co-location, and pruning |

The local checkouts live under `repos/`; [UPSTREAM.md](../../UPSTREAM.md) records their adopted revisions. The Effect checkout is version 4.0.4. OpenCode's reviewed dependency catalog uses 4.0.1, and T3 Code's uses 4.0.5. Resolve available APIs against the consuming project's declarations.

The [application examples](references/APPLICATIONS.md) route both codebases by the guarantee required. OpenCode covers dynamic graphs, reloads, shared execution and embedded hosting. T3 Code covers shared Layers, durable execution, ordered publication and replayable streams. Source links use absolute paths to these checkouts. A local link follows its checkout, so recheck claims when adopting another revision.

## Design Choices

The skill covers small programs, applications, framework integrations and reusable libraries. Guidance follows the operation, its callers and its owners. Services and Layers express useful capability, dependency and ownership boundaries; functions and composed Effects remain appropriate when those boundaries add no value. Reusable APIs preserve the caller's requirements and execution ownership.

Scoped internal refactoring is an explicit personal default: an implementation task can replace a concretely unsuitable Effect design, migrate its callers and remove the old path without compatibility scaffolding. Broader scope and externally breaking contracts require consultation unless already authorized.

The preference for `Schema.Struct` with a same-name interface is personal. Class schemas remain appropriate when their behavior helps. The per-error type brand is also a personal default, with its runtime and type contract described in Boundaries.

Application conventions are evidence to assess, not requirements to copy. OpenCode's graph compiler and retention policy address dynamic replacement and sharing. T3 Code's outbox and publication lane address durable admission and ordered delivery. Neither establishes a universal package layout, import style, service-per-file rule, persistence model or test runner.

## Validation

The embedded TypeScript examples were type-checked during their development. Eight isolated checks covered dependency capture, expected failures, schema rejection, scoped registration release, virtual time and reference-counted invalidation. Application checks below have narrower scopes than a full server or workspace test run.

### OpenCode

The source was reviewed on 2026-10-13 and 2026-10-14. Upstream regression tests were read, not executed. Bun and the OpenCode workspace dependencies were unavailable. Each workflow identifies implementation-only claims and missing direct acceptance cases.

On 2026-10-14, six isolated checks passed against the unmodified pinned `packages/sdk/src/internal/fetch.ts` on Node 24.19.0. Native TypeScript loading used a resolution hook for the module's extensionless self-export; no application graph or Effect dependencies were loaded. Checks verified that body exhaustion and handler failure release active request records and request-signal listeners; early body cancellation and host abort wait for gated underlying cancellation; caller abort rejects before a gated handler settles while close still waits; and repeated close shares one Promise and rejects new admission before disposal.

These checks exercise `OwnedFetch` only. Full host startup cleanup, plugin unload, encoded endpoint round trips and the upstream Bun suites were not executed.

### T3 Code

The source was reviewed on 2026-10-17. Persistence and worker regression tests were read, not executed.

Nine isolated upstream LiveStreamBudget tests passed on Node 24.21.0 with Effect 4.0.5, `@effect/vitest` 4.0.5 and Vitest 5.0.4. The implementation was copied unchanged to a temporary workspace. Only the test import from `vite-plus/test` was adapted to `vitest`; T3's runner patch was not applied. These tests cover item/serialized-byte limits, unacknowledged retention, source cleanup, blocked high-water/replay/projection and replay/live overlap. They do not validate real RPC acknowledgement, persistence, full startup/shutdown or worker recovery. Neither application checkout was changed.

## Forward Evaluation

### Application Host

On 2026-10-13, two fresh subagents with low reasoning effort implemented the same reloadable Promise-facing catalog task in isolated projects. Both passed the same eleven independent consumer acceptance cases covering connection ownership, coalescing, readiness, failure recovery, startup cleanup, and cancellation settlement.

The first used manual scope ownership and unknown failures while skipping Architecture and Boundaries. After clarifying guide routing, the application host boundary, and foreign-error translation, the fresh second run used a service, Layer, ManagedRuntime, and typed failure reasons.

This checks one application-host scenario. It does not establish a general success rate or isolate the effect of each wording change.

### Reusable Module

On 2026-10-14, a fresh subagent with xhigh reasoning implemented a bounded notification sender in an isolated project using this skill and Effect 4.0.4. The task was randomly selected from four general-use tasks. The agent received the public contract and skill, and chose the implementation; independent acceptance checks were withheld.

The 105-line module passed its 38 runtime tests, twelve independent consumer acceptance cases, and both project and independent type checks. Coverage included whole-batch validation before side effects, bounded concurrency, ordered results, transient retry limits, final error identity, cancellation settlement, and preservation of gateway requirements. The agent used schemas, bounded `Effect.forEach` and a Schedule, with caller-owned execution. Its tests also covered mixed failure/defect and failure/interruption causes.

This checks one reusable-module task. There was no comparison run without the skill, so the result does not isolate the skill's contribution or establish a general success rate.

## Maintenance

Review relevant implementation, examples and tests when adopting a source revision or changing guidance. Keep general rules in the topic guides and source evidence in the application examples. Validate instructions against realistic tasks, compile executable examples when they change, and test the ownership or concurrency contract affected. Preserve reference checkouts during ordinary work.

Earlier Effect sources included 4.0.1 revisions `b1d200c40a1dad69def51ebdbf0a1a612a12b8ac` and `757821fe99b7179f907d6d1a34a4e86de4173112`, and 4.0.3 revision `8aee3b9caa796aa79316c82c7c83f98c89dc49f5`. The adopted Effect source was reviewed on 2026-10-14 for GraphQL examples, HTTP retry and redaction, stream deadlines, schema and Match validation, interruption, workflow suspension and platform behavior. These records describe past evidence; ordinary application tasks do not need to repeat the source-adoption review.
