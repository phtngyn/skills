# OpenCode v2 Application Study

These studies describe the [cloned OpenCode v2 repository](/Users/phtngyn/Developer/skills/repos/opencode) on branch `v2` at `4617210822bdbb31e5749751afbfb4584ccedac8`, reviewed on 2026-10-13 and expanded on 2026-10-14. Its [dependency catalog](/Users/phtngyn/Developer/skills/repos/opencode/package.json) pins Effect and the Node platform adapter to 4.0.1. The skill's adopted Effect revision and executed checks are in [provenance](../PROVENANCE.md). Resolve API details against the consuming project's declarations; OpenCode supplies application evidence.

## Choose A Workflow

Study OpenCode v2 to learn how a substantial application uses Effect. The workflows below organize source evidence; their product features do not define the scope of this skill. Read a study when it helps explain a construction, ownership, failure or concurrency decision in the current task.

| General decision | Source study | OpenCode v2 workflow |
| --- | --- | --- |
| Service boundaries, dependency capture, global/location ownership, same-key execution, stop and settlement | [Session execution](OPENCODE_SESSION.md) | Submit a prompt while the session may already be running |
| Scoped subscribers, ordered replacement, coalescing, readiness, failure cleanup | [Plugin reload](OPENCODE_PLUGINS.md) | Change a plugin during boot or an active reload |
| Application host construction, Promise/Effect facades, stream lifetime, cancellation, encoding and shutdown | [Embedded host](OPENCODE_HOST.md) | Open an event stream and close its host while consumption is active |

Each study connects dependency capture, resource and fiber ownership, failure policy and caller guarantees to source evidence. Apply the relevant contract to the current task. OpenCode's package names, import rules, custom graph helpers, retention policy and Bun harness remain application conventions.

## Composition And Replacement

OpenCode declares services with `Context.Service`, implements them with Layers, and groups them into application graphs. Its [LayerNode compiler](/Users/phtngyn/Developer/skills/repos/opencode/packages/util/src/effect/layer-node.ts) resolves transitive replacements before acquisition, checks missing dependencies and cycles, and chooses memo maps for shared versus local subgraphs. [Ownership tags](/Users/phtngyn/Developer/skills/repos/opencode/packages/util/src/effect/app-node.ts) allow location nodes to depend on globals while globals cannot depend on location nodes through that graph API. [Instance.layer](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/instance.ts) compiles fresh location wiring on shared global dependencies.

**Lesson:** graph replacement must reach the actual adapter acquisition. Keep dependencies aligned with lifetime owners. Use ordinary Layers until repeated application requirements warrant more machinery; `LayerNode`, `makeGlobalNode`, and `makeLocationNode` are OpenCode helpers, not Effect exports. Their naming and import restrictions are house conventions.

The [replacement regression](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/effect/layer-node/layer-node.test.ts:155) records acquisitions and asserts that replaced dependencies and unused targets never start. The [session ownership study](OPENCODE_SESSION.md#put-each-owner-at-the-right-boundary) shows why a global capability routes to location services through a selector rather than retaining a location implementation.

## Keyed Service Graphs

[LocationServiceMap](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/location-service-map.ts) canonicalizes location keys. [buildLocationServiceMap](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/location-services.ts) uses `LayerMap` with infinite idle retention, removes failed builds to permit repair and retry, and checks build identity before delayed cleanup can evict a replacement. Invalidation detaches routing and invokes the old graph's shutdown while borrowers may still retain it. [LocationActivity](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/location-activity.ts) implements an additional inactivity policy: interrupt matching executions, await settlement, recheck for newly active work, then invalidate.

**Lesson:** resource cache lifetime, application inactivity, routing replacement, and active-work cancellation are separate contracts. A failed build with delayed cleanup needs generation-aware eviction when replacement is allowed. Adopt these details only for an application that needs them; infinite retention and custom sweeps are not defaults.

The adopted Effect checkout at `742976ce97f5157b00e67e4a5ece6bc04e1899e3` independently confirms that `LayerMap.invalidate` delegates to `RcMap.invalidate`, whose implementation removes routing immediately and closes an entry immediately only when its reference count is zero: [LayerMap.make](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/LayerMap.ts), [RcMap.invalidate](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/RcMap.ts:624).

## Regression Tests

Each workflow's regression table links the exact test, competing action and observable assertion. Those upstream tests were read as evidence of intended contracts; they were not run in this study. Bun and the OpenCode workspace dependencies were unavailable during the expansion. Implementation-only claims and missing direct acceptance cases are identified in each study.

Six isolated checks against the unmodified `OwnedFetch` source were executed on Node 24.19.0. They cover request release, gated body cancellation, handler settlement and close ordering; [provenance](../PROVENANCE.md#opencode-validation) records their scope. They do not execute the full embedded host or upstream Bun suite.

Additional cross-cutting sources were read:

- [location-layer.test.ts](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/location-layer.test.ts): repair and retry after failed boot, concurrent failed borrowers, and invalidated boot failures that must not evict replacement graphs.
- [test/lib/effect.ts](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/lib/effect.ts): Bun test integration with scoped execution, virtual/live services, and a replaceable HTTP capability that records forbidden network attempts even when application code catches them.

Transfer the observable failure scenarios into the consuming project's runner. Reusing the graph compiler or test harness is a separate engineering decision.

## Refresh

Recheck this study when adopting another OpenCode v2 revision or changing Effect versions. Fetch `v2` while preserving the reviewed checkout (`git -C /Users/phtngyn/Developer/skills/repos/opencode fetch origin v2`), compare revisions, and update provenance only after reviewing relevant implementation and tests. Local links follow the checkout, so keep it at the adopted v2 revision until that review is complete. No OpenCode dependencies are required to use this skill.
