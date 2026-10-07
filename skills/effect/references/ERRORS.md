# Errors And Recovery

## Three Failure Kinds

Expected recoverable failures belong in `Effect<A, E, R>`'s typed `E` channel. Defects represent unexpected bugs or violations; interruption represents cancellation. Catch expected failures with typed recovery (`catchTag`, `catchTags`, `catchIf`), rather than flattening every cause into a domain error.

Use cause-level handling only at a boundary that owns supervision or reporting. Preserve interruption, including mixed causes containing interrupts, unless the boundary explicitly owns a different policy. Cleanup and cancellation should not be reported as ordinary retryable failures.

## Error Representation

- `Schema.TaggedError`: errors requiring validation, persistence, encoding, transport contracts, or schema-derived tooling; a good application default for those boundaries.
- `Data.TaggedError`: internal typed failures that need no schema contract.
- `Schema.Error`: validated error class when a discriminator is unnecessary.

Choose meaningful failure names. Error tags need to be unambiguous within their union. Namespaced error tags may be an existing project convention, but are not universally required.

## Cause Versus Reason

An opaque `cause` preserves foreign exception evidence. A typed `reason` preserves distinctions callers can recover from. Use `Schema.Defect()` for opaque causes in schema-based errors, and a schema union for validated reasons. Do not serialize secrets or arbitrary internal exception payloads into public responses.

```ts
import { Effect, Schema } from "effect"

export class RateLimited extends Schema.TaggedError<RateLimited>()("RateLimited", {
  retryAfterMs: Schema.Finite,
}) {}

export class AccessDenied extends Schema.TaggedError<AccessDenied>()("AccessDenied", {}) {}

export class ProviderError extends Schema.TaggedError<ProviderError>()("ProviderError", {
  reason: Schema.Union([RateLimited, AccessDenied]),
}) {}

declare const request: Effect.Effect<string, ProviderError>

export const handled = request.pipe(
  Effect.catchReason("ProviderError", "RateLimited", (reason) =>
    Effect.succeed(`Retry after ${reason.retryAfterMs}ms`),
  ),
)
```

Use `catchReasons` for several reasons, or `unwrapReason` to move reasons into the error channel when the wrapper is no longer useful. Recover at the boundary with enough domain knowledge; a retry message is not itself a retry policy.

## Translation And Recovery

Translate errors where abstraction changes: a transport/SQL/SDK failure may become a provider or persistence error. Preserve typed causes/reasons needed by callers; avoid wrapping each service call mechanically when its existing failure already expresses the domain contract.

Use `Effect.try` and `tryPromise` for foreign APIs that throw/reject, mapping expected failures explicitly. `Effect.sync` treats throws as defects; use it when throwing represents a bug or when the operation cannot fail normally. For adapter cancellation, read [CONCURRENCY_STATE.md](CONCURRENCY_STATE.md).

Add operation labels and identifiers when they materially help diagnosis. Prefer spans/log annotations for observability over duplicating every operation name in every error payload. A shared error helper is useful only when several boundaries share the same translation semantics.

For retry policy, read [SCHEDULING.md](SCHEDULING.md); HTTP-specific classification is in [HTTP_CLIENTS.md](HTTP_CLIENTS.md).

At transport boundaries, map expected domain errors to deliberate status/payload contracts. Defects retain diagnostics at the owner; public clients receive an appropriate sanitized response. Keep successful absence (`Option`) distinct from a failure when absence is part of the domain.

## Source Anchors

At the source revision named in `SKILL.md`: `ai-docs/src/01_effect/04_errors/01_error-handling.ts`, `10_catch-tags.ts`, `20_reason-errors.ts`, and `packages/effect/src/http/HttpClientError.ts` (Data-based wrapper with typed reasons).
