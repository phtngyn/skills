# Caching, Memoization, And Request Dedupe

Prefer `effect/Cache` over a `Map` + timestamp + prune-loop cache when its keyed memoization, TTL, capacity, lifecycle, and eviction semantics fit.

## Core Rules

- `Cache.make({ capacity, lookup, timeToLive })` caches per-key lookups with one fixed TTL for all entries.
- `Cache.makeWith(lookup, { capacity, timeToLive(exit, key) })` computes TTL per entry from the lookup's `Exit` — the tool for "cache successes, not failures".
- Concurrent `Cache.get` calls for the same missing key share one pending lookup.
- `capacity` is required and bounds the cache.
- Return a zero TTL (`0` or `"0 millis"`) from `timeToLive` to avoid caching transient failures or degraded fallbacks without failing the caller. A short negative-cache TTL can be appropriate for stable failures such as not-found results.
- `Cache.invalidate(cache, key)` / `Cache.refresh(cache, key)` handle explicit staleness; `Cache.has` checks without triggering a lookup.
- Cache construction is effectful. Build the cache once in the owning layer/scope and share the handle; a cache built per call caches nothing.
- Lookup services are captured at construction by default. Use `requireServicesAt: "lookup"` only when callers should supply them on each lookup; this changes the cache's environment type.
- `timeToLive` is optional and defaults to infinity. Specify it when freshness matters; capacity alone only bounds retained entries.
- For a single value (no key), use `Effect.cached(effect)` or `Effect.cachedWithTTL(effect, ttl)` instead of a one-key Cache.
- For cached resources that need cleanup (connections, clients), use `ScopedCache`.

## Exit-Aware TTL (cache successes, skip degraded results)

```ts
import { Cache, Duration, Effect, Exit } from "effect"

const makeResolver = Effect.gen(function* () {
  const cache = yield* Cache.makeWith(
    (channelRef: string) => resolveUncached(channelRef), // never-failing, returns { where, cacheable }
    {
      capacity: 300,
      timeToLive: (exit) =>
        Exit.isSuccess(exit) && exit.value.cacheable ? "10 minutes" : Duration.zero,
    },
  )
  return (channelRef: string) =>
    Cache.get(cache, channelRef).pipe(Effect.map((resolved) => resolved.where))
})
```

## Resource Acquisition

Acquire clients once in their owning layer, outside the lookup. Read [RESOURCES_RUNTIME.md](RESOURCES_RUNTIME.md) for layer sharing and scoped acquisition.

## Request Batching (`Effect.request` + `RequestResolver`)

Batching exists for backends with a real batch endpoint: the resolver receives an array of pending requests and can collapse them into one wire call.

- Use it when the API can answer N keys in one call (SQL `IN (...)`, DataLoader-style endpoints, batch GET).
- Do not reach for it when the backend only has per-item endpoints (most REST provider APIs): a batched resolver still loops one call per entry, so it buys nothing over `Effect.forEach(items, f, { concurrency })` plus `Cache` for dedupe/memoization.
- `RequestResolver.batchN(resolver, n)` bounds batch size; `RequestResolver.makeGrouped` groups requests that must resolve through different targets.

Selection guide:

- Same key requested repeatedly over time → `Cache`.
- Same key requested concurrently in one burst → `Cache` (shared pending lookup).
- Many distinct keys, backend has a batch endpoint → `Effect.request` + `RequestResolver`.
- Many distinct keys, per-item endpoint only → `Effect.forEach(..., { concurrency: n })`, optionally through a `Cache`.
