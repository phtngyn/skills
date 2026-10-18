# Operations

## Retry And Deadlines

Retry where failure is transient and repetition is safe. Establish idempotency or deduplication for side effects. Bound attempts or elapsed time, retain exhausted failures and use a fallback only when it represents a truthful result.

`Effect.retry` repeats typed failure; `repeat` repeats success. `Schedule.recurs(n)` permits n additional runs after the first. Use delay schedules for polling or backoff, jitter where workers can synchronize, and provider delays such as Retry-After where applicable. Inspect built-in HTTP retry classification and bounds before enabling it.

For a recurring worker, decide whether an expected pass failure is reported and skipped, retried or stops the worker. Defects and cancellation need the supervisor's policy. For a batch, isolate item failures only when that matches the product contract.

Decide whether a deadline includes queueing, acquisition, retries and cleanup. A timed-out foreign operation can remain active when its adapter ignores abort; see [Boundaries](BOUNDARIES.md#adapt-foreign-apis).

## Caching And Batching

| Requirement | Mechanism to assess |
| --- | --- |
| One retained computation | `Effect.cached` / `cachedWithTTL` |
| Bounded keyed results | `Cache` |
| Keyed resources with release | `ScopedCache` / `RcMap` |
| Keyed service graphs | `LayerMap` |
| Backend accepts batched requests | `Request` / `RequestResolver` |
| Backend only supports per-item calls | Bounded `forEach` |

Construct a cache at its owner. Define identity, authority, freshness, capacity and failure retention. An Exit-aware TTL can avoid retaining transient failures or successful degraded fallbacks. Verify whether lookup dependencies are captured at construction or supplied on invocation.

A bounded result cache can evict an in-flight entry and allow another lookup for that key. If single-flight behavior must survive eviction, pending-work ownership needs its own contract. Batching helps when requests share a backend operation; separate authority domains and respect batch limits.

## External I/O And Persistence

Configure HTTP credentials, base URL, status classification and decoding at the adapter. Keep authoritative transactions limited to facts that must commit together. External I/O has its own retry and ambiguous-outcome policy.

Process-owned fibers provide local supervision. If intent must survive process loss, assess the release's durable workflow tools or an appropriate persisted-work protocol. Store required work with authoritative state when a crash between them would lose the operation. Acceptance and completed execution are different promises.

Deduplicating admission does not guarantee exactly-once external execution. Success followed by failed settlement needs replay, reconciliation or terminal-failure policy appropriate to the adapter. In-memory wakeups accelerate discovery while durable state supports recovery.

For resumable synchronization, preserve stable identity, observe actual state and apply managed deltas toward desired state. Stored properties cannot prove current external state or authorize adoption. Classify conflicts and read-after-write failures per operation and bound retries.

If consumers advance monotonic cursors, coordinate publication order across commit and notification. A local semaphore only coordinates local participants. Required recovery work must survive a process exit; post-commit notifications alone cannot establish that guarantee.

## Observability And Time

Name spans after useful operations and add bounded identifiers that answer operational questions. Avoid reporting the same failure at every layer or using high-cardinality metric labels. Configure exporters and their cleanup at the application owner.

Use Clock-backed time so retry, TTL, polling and deadlines can be tested. Use `DateTime` where parsing, zones or calendar arithmetic matter; distinguish instants, durations and local calendar values. A fixed offset cannot model daylight-saving rules.

Keep secrets and private payloads out of logs, public errors, spans and labels. Inspect a client's redaction defaults before replacing them; application-specific redaction must retain any defaults still required.
