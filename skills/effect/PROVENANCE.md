# Effect Provenance

This personal skill teaches design and implementation decisions for Effect v4. Its organization and defaults are our synthesis; Effect source establishes API behavior, and OpenCode supplies application evidence.

## Reviewed Sources

| Source | Reviewed revision | Material used |
| --- | --- | --- |
| Effect | [`8aee3b9caa796aa79316c82c7c83f98c89dc49f5`](https://github.com/Effect-TS/effect/tree/8aee3b9caa796aa79316c82c7c83f98c89dc49f5) | `LLMS.md`, focused application examples, public declarations/implementation, and test/type-test conventions |
| OpenCode v2 | [`4617210822bdbb31e5749751afbfb4584ccedac8`](https://github.com/anomalyco/opencode/tree/4617210822bdbb31e5749751afbfb4584ccedac8) | Service graph composition, location ownership, plugin registrations, reloads, session coordination, host adapters, and focused regression tests |
| Writing for Agents | [`49dd158d1076134a641b33efb035946536778336`](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336) | Decision-oriented hierarchy, conditional context pointers, co-location, and pruning |

The local checkouts live under this collection's `repos/`; [UPSTREAM.md](../../UPSTREAM.md) records their adopted revisions. Topic guides point directly to the material used. The [OpenCode study](references/OPENCODE.md) retains immutable source links and describes what was reviewed rather than claiming an exhaustive audit.

The earlier handbook was developed from Effect 4.0.1 revisions `b1d200c40a1dad69def51ebdbf0a1a612a12b8ac` and `757821fe99b7179f907d6d1a34a4e86de4173112`. The current rewrite was reviewed against the Effect 4.0.3 checkout above. Historical revision records are provenance, not steps an agent must repeat before ordinary application work.

## Design Choices

The skill defaults to applications, organized by domain capabilities and explicit ownership. Its plain-record preference for `Schema.Struct` plus a same-name interface is personal; class schemas remain appropriate when their behavior helps. Public-library machinery loads only for reusable consumer contracts.

OpenCode demonstrates the consequences of ownership and concurrency policy in a substantial application. Its graph compiler, package layout, import restrictions, infinite resource retention, and custom test runner are examples to reason from, not requirements to copy.

The rewrite replaces the API-by-topic handbook with guides for architecture, boundaries, lifetimes, concurrency, operations, testing, and libraries. Source lookup supports uncertain choices; routine revision comparison and legacy migration catalogs are removed.

## Updating

Review the relevant implementation, examples, and tests when adopting another source revision or changing guidance. Keep a rule in one guide and use conditional links from other guides. Validate instructions by tracing realistic tasks, compile executable examples when they change, and check meaningful behavior for ownership and concurrency claims.

These references are a focused synthesis, not a substitute for the consuming project's declarations, tests, or conventions. Preserve reference checkouts during ordinary work. The rewrite's embedded TypeScript examples were type-checked, and eight isolated tests covered dependency capture, expected failures, schema rejection, scoped registration release, virtual time, and reference-counted invalidation. OpenCode's upstream regression tests were read; they were not executed as part of the study.

## Forward Evaluation

On 2026-10-13, two fresh subagents with low reasoning effort implemented the same reloadable Promise-facing catalog task in isolated projects. Both passed the same eleven independent consumer acceptance cases covering connection ownership, coalescing, readiness, failure recovery, startup cleanup, and cancellation settlement.

The first used manual scope ownership and unknown failures while skipping Architecture and Boundaries. After clarifying guide routing, the application host boundary, and foreign-error translation, the fresh second run used a service, Layer, ManagedRuntime, and typed failure reasons.

This checks one application-host scenario. It does not establish a general success rate or isolate the effect of each wording change.
