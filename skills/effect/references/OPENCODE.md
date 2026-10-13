# OpenCode v2 Application Study

Reviewed the `v2` branch at `4617210822bdbb31e5749751afbfb4584ccedac8` on 2026-10-13, cloned at `repos/opencode` in this collection. Its [dependency catalog](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/package.json) pins Effect and the Node platform adapter to 4.0.1. This is a focused source review, not an audit or a report of executed upstream tests. Effect's public declarations and implementation remain the API authority.

## Composition And Replacement

OpenCode declares services with `Context.Service`, implements them with Layers, and groups them into application graphs. Its [LayerNode compiler](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/util/src/effect/layer-node.ts) resolves transitive replacements before acquisition, checks missing dependencies and cycles, and chooses memo maps for shared versus local subgraphs. [Ownership tags](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/util/src/effect/app-node.ts) allow location nodes to depend on globals while globals cannot depend on location nodes through that graph API. [Instance.layer](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/src/instance.ts) compiles fresh location wiring on shared global dependencies.

**Lesson:** graph replacement must reach the actual adapter acquisition. Keep dependencies aligned with lifetime owners. Use ordinary Layers until repeated application requirements warrant more machinery; `LayerNode`, `makeGlobalNode`, and `makeLocationNode` are OpenCode helpers, not Effect exports. Their naming and import restrictions are house conventions.

## Keyed Service Graphs

[LocationServiceMap](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/src/location-service-map.ts) canonicalizes location keys. [buildLocationServiceMap](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/src/location-services.ts) uses `LayerMap` with infinite idle retention, removes failed builds to permit repair and retry, and checks build identity before delayed cleanup can evict a replacement. Invalidation detaches routing and invokes the old graph's shutdown while borrowers may still retain it. [LocationActivity](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/src/location-activity.ts) implements an additional inactivity policy: interrupt matching executions, await settlement, recheck for newly active work, then invalidate.

**Lesson:** resource cache lifetime, application inactivity, routing replacement, and active-work cancellation are separate contracts. A failed build with delayed cleanup needs generation-aware eviction when replacement is allowed. Adopt these details only for an application that needs them; infinite retention and custom sweeps are not defaults.

The reviewed Effect checkout at `8aee3b9caa796aa79316c82c7c83f98c89dc49f5` independently confirms that `LayerMap.invalidate` delegates to `RcMap.invalidate`, whose implementation removes routing immediately and closes an entry immediately only when its reference count is zero: [LayerMap.make](https://github.com/Effect-TS/effect/blob/8aee3b9caa796aa79316c82c7c83f98c89dc49f5/packages/effect/src/LayerMap.ts), [RcMap.invalidate](https://github.com/Effect-TS/effect/blob/8aee3b9caa796aa79316c82c7c83f98c89dc49f5/packages/effect/src/RcMap.ts).

## Scoped Registrations

[PluginHooks.register](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/src/plugin/hooks.ts) requires `Scope`, registers removal in that scope, and returns an idempotent `dispose` Effect. The [public registration contract](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/plugin/src/effect/registration.ts) exposes that ownership to plugin authors. The registry outlives individual plugins; hook invocation yields callback effects in the triggering workflow.

**Lesson:** a registration's owner is the subscriber. Invocation and background work need their own explicit fiber policies. Model hook failure permissions per operation instead of giving every callback a broad failure union.

## Reload And Readiness

The [plugin supervisor](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/src/plugin/supervisor.ts) starts source subscriptions before activation, retains the newest pending trigger in `Queue.sliding(1)`, and uses one `Stream.runForEach` consumer. Initial activation runs immediately; later triggers are debounced. Accepted/settled generation tracking keeps readiness blocked when another change arrived during activation. Separately forked update checks guard against publishing stale generations.

**Lesson:** debounce does not serialize work. A sliding queue fits reloads that recompute current state and can discard intermediate notifications. Readiness should describe all accepted work, not merely completion of one activation.

## Promise And Stream Boundaries

The [Promise plugin adapter](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/plugin/src/promise/adapter.ts) captures the plugin context for registrations and Effect execution, passes abort signals for supported calls, and tracks async iterators for closure on plugin unload. Its schema-based endpoint adapter preserves the Promise client's encoded contract rather than exposing internal decoded values directly.

The [embedded host](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/sdk/src/internal/host.ts) owns a `ManagedRuntime` and disposes it if startup fails. [OwnedFetch](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/sdk/src/internal/fetch.ts) tracks requests through response-body completion, rejects calls after close starts, aborts active requests, awaits their settlement, and then disposes the runtime.

**Lesson:** crossing into Promises also crosses cancellation, representation, and ownership contracts. A resolved streaming response has not finished using its resources. Keep bridge execution at the host/foreign API boundary and choose each call's lifetime explicitly.

## Regression Tests

These tests were read as evidence of intended contracts; they were not run in this study:

- [location-layer.test.ts](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/test/location-layer.test.ts): repair and retry after failed boot, concurrent failed borrowers, and invalidated boot failures that must not evict replacement graphs.
- [supervisor-reload.test.ts](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/test/plugin/supervisor-reload.test.ts): a change while initial activation is gated, periodic refresh serialized behind an in-flight reload, and retention of the running generation after import failure.
- [plugin-failure.test.ts](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/test/plugin-failure.test.ts): removal of failed-plugin hooks and RPC handlers, healthy-peer continuity, and readiness/teardown interactions.
- [test/lib/effect.ts](https://github.com/anomalyco/opencode/blob/4617210822bdbb31e5749751afbfb4584ccedac8/packages/core/test/lib/effect.ts): Bun test integration with scoped execution, virtual/live services, and a replaceable HTTP capability that records forbidden network attempts even when application code catches them.

Prefer these failure scenarios over copying the custom test harness. Your project runner and matching Effect exports determine the implementation.

## Refresh

Recheck this study when adopting another OpenCode revision or changing Effect versions. Fetch `v2` while preserving the reviewed checkout (`git -C repos/opencode fetch origin v2`), compare revisions, and update provenance only after reviewing relevant implementation and tests. No OpenCode dependencies are required to use this skill.
