# Effect Provenance

This personal skill teaches design and implementation decisions for Effect v4. Its organization and defaults are our synthesis; Effect source establishes API behavior, and OpenCode supplies application evidence.

## Reviewed Sources

| Source | Reviewed revision | Material used |
| --- | --- | --- |
| [Effect](/Users/phtngyn/Developer/skills/repos/effect) | `742976ce97f5157b00e67e4a5ece6bc04e1899e3` | `LLMS.md`, focused application examples, public declarations/implementation, and test/type-test conventions |
| [OpenCode v2](/Users/phtngyn/Developer/skills/repos/opencode) | `4617210822bdbb31e5749751afbfb4584ccedac8` | Service graph composition, location ownership, plugin registrations, reloads, session coordination, host adapters, and focused regression tests |
| [Writing for Agents](/Users/phtngyn/Developer/skills/repos/mattpocock) | `49dd158d1076134a641b33efb035946536778336` | Decision-oriented hierarchy, conditional context pointers, co-location, and pruning |

The local checkouts live under this collection's `repos/`; [UPSTREAM.md](../../UPSTREAM.md) records their adopted revisions. Topic guides point directly to the material used. The [OpenCode v2 study](references/OPENCODE.md) provides architectural evidence through session execution, plugin reload and embedded hosting. Source links use absolute paths to the cloned repositories, with line locators where useful. Reviewed revisions remain recorded here; a local path follows its checkout, so recheck claims when adopting another revision.

The earlier handbook was developed from Effect 4.0.1 revisions `b1d200c40a1dad69def51ebdbf0a1a612a12b8ac` and `757821fe99b7179f907d6d1a34a4e86de4173112`. The rewrite was initially reviewed against Effect 4.0.3 at `8aee3b9caa796aa79316c82c7c83f98c89dc49f5`. On 2026-10-14, the adopted checkout advanced to the revision above (package version 4.0.4), with focused review of GraphQL examples, HTTP retry and redaction, stream deadlines, schema and Match validation, interruption, workflow suspension, and platform changes. Historical revision records are provenance, not steps an agent must repeat before ordinary application work.

## Design Choices

The skill covers small programs, applications, integrations and reusable libraries. Guidance follows the current operation, its callers and owners. Services and Layers are introduced for useful capability, dependency and ownership boundaries. Its plain-record preference for `Schema.Struct` plus a same-name interface is personal; class schemas remain appropriate when their behavior helps. Public-library machinery loads only for reusable consumer contracts.

OpenCode demonstrates the consequences of ownership and concurrency policy in a substantial application. Its graph compiler, package layout, import restrictions, infinite resource retention, and custom test runner are examples to reason from, not requirements to copy.

On 2026-10-14, the pinned OpenCode v2 study expanded from mechanism summaries into workflows through admission, construction, execution, replacement and teardown. It connects each requirement to its Effect mechanism and observable contract. Regression tables distinguish test evidence from implementation review. The consuming task supplies its own domain and architecture.

The rewrite replaces the API-by-topic handbook with guides for architecture, boundaries, lifetimes, concurrency, operations, testing, and libraries. Source lookup supports uncertain choices; routine revision comparison and legacy migration catalogs are removed.

## Updating

Review the relevant implementation, examples, and tests when adopting another source revision or changing guidance. Keep a rule in one guide and use conditional links from other guides. Validate instructions by tracing realistic tasks, compile executable examples when they change, and check meaningful behavior for ownership and concurrency claims.

These references are a focused synthesis, not a substitute for the consuming project's declarations, tests, or conventions. Preserve reference checkouts during ordinary work. The rewrite's embedded TypeScript examples were type-checked, and eight isolated tests covered dependency capture, expected failures, schema rejection, scoped registration release, virtual time, and reference-counted invalidation. OpenCode's upstream regression tests were read; they were not executed as part of the study. Transport checks executed during the expansion are recorded below.

## OpenCode Validation

On 2026-10-14, six isolated checks passed against the unmodified pinned `packages/sdk/src/internal/fetch.ts` on Node 24.19.0. Native TypeScript loading used a resolution hook for the module's extensionless self-export; no application graph or Effect dependencies were loaded. Checks verified body exhaustion and handler failure release active request records and request-signal listeners; early body cancellation and host abort wait for gated underlying cancellation; caller abort rejects before a gated handler settles while close still waits; and repeated close shares one Promise and rejects new admission before disposal.

These checks exercise `OwnedFetch` only. Full host startup cleanup, plugin unload, encoded endpoint round trips and the upstream Bun suites were not executed. Bun and the OpenCode workspace dependencies were unavailable. The studies identify implementation-only claims separately.

## Forward Evaluation

### Application Host

On 2026-10-13, two fresh subagents with low reasoning effort implemented the same reloadable Promise-facing catalog task in isolated projects. Both passed the same eleven independent consumer acceptance cases covering connection ownership, coalescing, readiness, failure recovery, startup cleanup, and cancellation settlement.

The first used manual scope ownership and unknown failures while skipping Architecture and Boundaries. After clarifying guide routing, the application host boundary, and foreign-error translation, the fresh second run used a service, Layer, ManagedRuntime, and typed failure reasons.

This checks one application-host scenario. It does not establish a general success rate or isolate the effect of each wording change.

### Reusable Module

On 2026-10-14, a fresh subagent with xhigh reasoning implemented a bounded notification sender in an isolated project using this skill and Effect 4.0.4. The task was randomly selected from four general-use tasks. The agent received the public contract and skill, and chose the implementation; independent acceptance checks were withheld.

The 105-line module passed its 38 runtime tests, twelve independent consumer acceptance cases, and both project and independent type checks. Coverage included whole-batch validation before side effects, bounded concurrency, ordered results, transient retry limits, final error identity, cancellation settlement, and preservation of gateway requirements. The agent used schemas, bounded `Effect.forEach` and a Schedule, with caller-owned execution. Its tests also covered mixed failure/defect and failure/interruption causes.

This checks one reusable-module task. There was no comparison run without the skill, so the result does not isolate the skill's contribution or establish a general success rate.
