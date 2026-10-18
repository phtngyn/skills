# Boundaries

## Decode And Encode Deliberately

Decode unknown HTTP, file, database, event or SDK representations at the boundary that owns them. Carry trusted domain values inward. Encode when the outward contract differs from the internal representation, including in-process facades that promise wire-format values.

```ts
import { Schema } from "effect"

export const User = Schema.Struct({
  id: Schema.String,
  name: Schema.NonEmptyString,
  email: Schema.optionalKey(Schema.String),
})
export type User = typeof User.Type
export const decodeUser = Schema.decodeUnknownEffect(User)
```

A Struct describes a record; `Schema.Class` adds constructor behavior and class identity when useful. Follow the project's model conventions. Brand scalars when mixing otherwise identical values would be a domain mistake; use discriminated variants when behavior depends on the case.

Distinguish absent keys, explicit undefined, null and domain absence. Constructor defaults and decoded transformations serve different jobs. `schema.make` applies constructor defaults and type-side validation, and can throw; an Effect decoder keeps input rejection in the error channel. Check the selected constructor or parser before translating its failure.

## Preserve Failure Meaning

Typed errors describe expected failures; defects describe bugs or broken assumptions; interruption describes cancellation. Successful absence can use `Option` or the domain's established representation.

Use tagged errors when callers discriminate cases. `Data.TaggedError` works for internal failures; schema-backed errors are useful when validation or encoding is part of the contract. Nominal brands and class identity are choices justified by the public type contract, rather than requirements for every error.

Translate failures when the abstraction changes. Keep an existing error when it already expresses the caller's contract. At a raw foreign boundary, accept `unknown` and map expected failures to a meaningful error while retaining opaque evidence in `cause`. Avoid widening a useful domain error channel to `unknown`.

Use typed recovery for expected failures. At supervision and reporting boundaries, inspect the complete Cause when cleanup, concurrent failure or interruption matters. Verify the selected release's mixed-cause behavior; recovering one typed failure must not silently erase other failures that the owner promises to report. Preserve cancellation through recovery and retry unless the owner deliberately handles it.

Use `try` / `tryPromise` for expected foreign throws or rejections. `sync` / `promise` treat unexpected throws or rejections as defects. Use `orDie` where a lower-level failure is an invariant violation for this caller.

## Adapt Foreign APIs

A network adapter owns request construction, credentials, status classification, body decoding and error translation. Classify status before decoding a success payload. Retry where repeating the operation is known to be safe.

Pass Effect's AbortSignal into cooperative APIs. Subscription adapters register listener removal or cancellation with their owner. An interrupted wrapper cannot stop an API that ignores cancellation; distinguish prompt caller cancellation from underlying settlement. Streaming bodies and iterators can outlive the Promise that returned them; see [Lifetimes](LIFETIMES.md#runtime-and-stream-boundaries).

Transport adapters map expected errors to deliberate status and payload contracts. Keep secrets and internal exception evidence out of public responses.

## Match Configuration To Its Lifetime

Read stable configuration through `Config` and provider Layers during construction. Supply dynamic or invocation-specific configuration at its actual owner; do not freeze request authority or changing settings into a process-wide service. Keep ambient environment reads out of domain logic.

Use `Context.Reference` for settings with legitimate defaults and required services for authority or dependencies that must be supplied. Use redacted values for credentials and refined schemas where input constraints matter. `Config.withDefault` handles missing values; malformed values still fail.

Tests can provide a `ConfigProvider` when exercising decoding, or supply already-decoded configuration for domain workflows.
