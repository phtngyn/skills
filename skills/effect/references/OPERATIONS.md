# Operations

## Retry And Deadlines

Retry the operation that knows the failure is transient and repeating is safe. Establish idempotency or deduplication for side effects. Bound attempts or elapsed time, preserve exhausted failures, and choose a fallback only when it is a truthful result.

`Effect.retry` retries typed failures; `repeat` repeats success. The source runs before the schedule steps. `Schedule.recurs(n)` allows n additional runs after the first. Use delay schedules for backoff/polling, add jitter where many workers can synchronize, and respect provider delays such as Retry-After. `spaced` waits after work; `fixed` follows a cadence.

For a recurring worker, decide whether an expected pass failure is reported and skipped, retried, or stops the worker. For a batch, isolate item failures only when skipping or later retry matches the product policy. Defects and cancellation need the supervisor's policy, not broad conversion into an operational retry.

Place deadlines around the useful operation. Decide whether the budget includes queue time, acquisition, retries, and cleanup. A timed-out foreign operation may still be running if its adapter ignores abort; [Boundaries](BOUNDARIES.md#foreign-and-transport-adapters) covers cancellation propagation.

Evidence: [Schedule](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Schedule.ts), [Effect retry/repeat/timeout](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Effect.ts).

## Caching And Batching

| Requirement | Mechanism |
| --- | --- |
| One memoized value | `Effect.cached` / `cachedWithTTL` |
| Bounded keyed results | `Cache` |
| Keyed resources with release actions | `ScopedCache` / `RcMap`, according to borrowing semantics |
| Keyed service graphs | `LayerMap`; see [Lifetimes](LIFETIMES.md#sharing-and-keyed-graphs) |
| Backend accepts several requests in one call | `Request` / `RequestResolver` |
| Backend has only per-item operations | Bounded `forEach`, optionally through a result cache |

Construct a cache once at its owner. Define key identity, freshness, capacity, and what happens to failed/degraded results. Exit-aware TTL allows a short or zero retention for transient failures; successful fallbacks can also need zero retention. Keep required credentials/configuration in the ownership and key design.

`Cache` shares a pending lookup while the entry remains retained. Capacity eviction can remove a pending entry and permit another lookup for that key. When single-flight behavior must survive capacity churn, separate pending-work coordination from bounded result retention. Verify the library's service-capture policy when constructing a lookup that needs dependencies.

For GraphQL, read the [native batching examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/52_graphql): `GraphQLResolver` supports list-key operations and aliased single-item queries. Separate batches by request authority when middleware depends on per-request services, and bound batch size by backend limits.

Batching is useful when the backend can answer many inputs in one operation. Group by the actual target and bound batch size. A resolver that makes one network request per item supplies no batch endpoint benefit by itself.

Evidence: [Cache](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Cache.ts), [ScopedCache](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/ScopedCache.ts), [RequestResolver](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/RequestResolver.ts).

## External I/O And Persistence

Prefer native Effect HTTP/platform services when their contracts fit. Configure auth/base URL and classify non-success status before response decoding. Built-in transient retry and rate limiting are policies: inspect their status classification, retry bounds, and idempotency implications before enabling them. `HttpClient.retryTransient` treats Retry-After as a minimum delay alongside the selected schedule; set retry bounds and a deadline that fit the operation. Some helpers include retry behavior and may default to unlimited retries.

## Durable Work And Publication

Keep authoritative database transactions limited to the facts that must commit together. External I/O needs its own retry and idempotency policy outside that transaction. Fiber supervision supplies process-local ownership; crash recovery requires persisted intent and a recovery protocol.

When supported by the consuming client, use `SqlClient.afterCommit` for short wakeups, cache invalidation or subscriber notifications. Buffered callbacks run after the outermost transaction commits. Callbacks registered in a transaction or savepoint that rolls back are discarded. Outside a transaction they run immediately. Check driver support: transactions outside the standard transaction wrapper can also run callbacks immediately. After commit, callbacks run uninterruptibly, and `withTransaction` waits for them to finish. Keep them short. They can be lost on process exit, so required durable work still belongs in the transaction's outbox.

When committed intent must survive a crash, an outbox can atomically store state changes and required work, then execute external I/O after commit. Distinguish accepted intent from completed execution. Deduplicating admission does not make external execution exactly-once: success followed by failed settlement needs an explicit replay, reconciliation or terminal-failure policy based on the adapter's idempotency contract. Process-bound handles may require a different recovery policy from replay-safe work. In-memory notifications accelerate discovery; durable rows remain authoritative.

Commit order also does not automatically establish live publication order. If consumers advance monotonic cursors, coordinate or reconstruct ordered publication across the commit-to-notify handoff. A local semaphore only coordinates its local participants. The [T3 Code example](T3_CODE.md#separate-durable-acceptance-from-execution) traces admission and recovery, and its [publication workflow](T3_CODE.md#preserve-publication-order-explicitly) traces the ordering handoff. Use a scoped worker or finite operation when crash recovery is outside the task's requirements.

Evidence: [HttpClient](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/http/HttpClient.ts), [SQL examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/40_sql), [SqlClient.afterCommit](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/sql/SqlClient.ts), [OpenCode session admission and execution](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/execution.ts).

## Observability And Time

Name spans after meaningful operations with `Effect.fn`. Add structured identifiers that explain a request or job; avoid reporting the same failure at every layer. Configure loggers, exporters, and their release actions at the application owner. Choose metrics for an operational question and keep label cardinality bounded.

Use Clock-backed time in Effect workflows so tests can control it. Use `DateTime` for instants, parsing, zones, and calendar arithmetic; distinguish durations and local calendar values in the model. A fixed offset cannot describe a zone's daylight-saving rules. Make ambiguous/nonexistent local-time policy explicit when the feature encounters it.

Use virtual time for deadlines, retry, TTL, and polling checks. Use real time only when it is the integration behavior being tested. Keep secrets and private payloads out of logs, spans, error responses, and metric labels. Configure `UrlParams.CurrentRedactedNames` for application-specific sensitive query keys. A custom list replaces the defaults, so include defaults still needed. Its patterns govern HTTP URL inspection, spans, and errors, while outgoing requests retain their values.

Evidence: [observability examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/08_observability), [DateTime examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/07_datetime), [Clock](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Clock.ts), [query parameter redaction](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/http/UrlParams.ts).
