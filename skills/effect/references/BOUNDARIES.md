# Boundaries

## Decode, Decide, Encode

Decode unknown HTTP, file, database, event, or SDK representations at the boundary that owns them. Carry trusted domain values inward. Encode explicitly when the outward contract differs from the internal type, including at an in-process Promise facade that promises wire-format values.

For ordinary records, this skill prefers a Struct and same-name interface:

```ts
import { Schema } from "effect"

export const User = Schema.Struct({
  id: Schema.String,
  name: Schema.NonEmptyString,
  email: Schema.optionalKey(Schema.String),
})
export interface User extends Schema.Schema.Type<typeof User> {}

export const decodeUser = Schema.decodeUnknownEffect(User)
```

Use `Schema.Class` when constructor behavior, methods, or class identity help the model. Brand scalar values when mixing otherwise identical representations would be a domain mistake. Model legal variants with a discriminated union: `Data.TaggedEnum` for internal control flow, schema-backed variants when validation or encoding is required.

Distinguish absent keys (`optionalKey`), explicit undefined, null, and domain absence. Normalize defaults into required domain fields. Reuse fields when two contracts share meaning; map explicitly when their behavior differs. Add schema identifiers when diagnostics or tooling use them.

`schema.make` constructs a trusted type-side value; decoding interprets an unknown encoded representation. Constructor defaults and decoded transformations have different jobs. Prefer Effect decoding when failure belongs in the workflow; use Option/Result decoders when a pure caller deliberately discards or handles validation details. Low-level constructor/parser errors can differ from `SchemaError`; check the selected operation before translating them.

Evidence: [schema examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/02_schema/10_schema-basics.ts), [Schema](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Schema.ts). For an in-process Promise facade promising client representations, read [OpenCode endpoint encoding](OPENCODE_HOST.md#plugin-context-iterators-and-representation).

## Errors Callers Can Act On

| Outcome | Representation and handling |
| --- | --- |
| Expected failure | Typed `E`, with a meaningful tag or reason callers can recover from |
| Broken invariant or unexpected bug | Defect, retaining diagnostic evidence for the owner |
| Cancelled work | Interruption, preserving cancellation through recovery and shutdown |
| Successful absence | `Option` or the domain's chosen absence representation |

Use `Data.TaggedError` for internal failures without a serialization contract. Use `Schema.TaggedError` when errors cross validated, persisted, or transport boundaries. Tags distinguish cases within the relevant union. Add a typed `reason` when callers need specific recovery decisions; an opaque `cause` retains foreign exception evidence.

For schema-backed error classes, this skill prefers a per-class type brand through the second generic:

```ts
export class NotFound extends Schema.TaggedError<NotFound, { readonly brand: unique symbol }>()(
  "NotFound",
  { id: Schema.String },
) {}
```

The tag distinguishes union cases; the brand prevents structurally matching values from satisfying the error class type. The `Brand` generic adds a type-only member, so constructor inputs and encoded payloads still contain only the schema fields. Decode transport values through the class schema to obtain instances. Verify this contract with a negative type check for a structurally matching value and a runtime encode/decode round trip that preserves class identity and omits the brand from both the instance and payload.

Evidence: [Schema.ts](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Schema.ts) (`TaggedError`'s `Brand` generic and implementation). Recheck the generic when upgrading Effect.

Translate where the abstraction changes, such as HTTP/SQL failure into a domain capability error. Keep the original error when it already expresses the caller's contract. A wrapper that hides distinctions without adding meaning weakens recovery.

Accept `unknown` at the raw foreign boundary, then translate it into a named failure before returning the domain Effect. Preserve opaque evidence in a `cause: unknown` field without widening the whole error channel to `unknown`. Internal waiters and coordination should preserve the same error contract.

Use `catchTag` or another typed recovery for expected failures. Use cause-level recovery at the boundary that owns supervision or reporting, with an explicit interruption policy. Preserve mixed causes containing interruption unless that owner deliberately handles them. Cancellation should not silently become a successful fallback or retryable domain error.

The reviewed runtime promotes ordinary typed failures to defects when combining them with defects from finalizers or concurrent siblings. Typed recovery must not hide a crashing finalizer or sibling. At a reporting boundary, inspect the complete Cause instead of extracting one expected error and discarding the remaining reasons. Verify this behavior against the consuming project's Effect version when recovery depends on it.

Use `try` / `tryPromise` around foreign operations whose throws/rejections are expected failures. `sync` / `promise` represent unexpected throws/rejections as defects. `orDie` belongs where an expected lower-level failure is an invariant violation for this caller; it is not a way to satisfy a narrower method signature.

Evidence: [error handling](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/04_errors/01_error-handling.ts), [typed reasons](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/04_errors/20_reason-errors.ts), [failure and finalization regressions](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/test/Effect.test.ts).

## Foreign And Transport Adapters

A network adapter owns request construction, credentials, execution, status classification, body decoding, and error translation. Classify status before decoding success payloads. Keep retry policy at the boundary that knows whether repeating the operation is safe; read [Operations](OPERATIONS.md#retry-and-deadlines).

Pass the Effect-provided AbortSignal into cooperative foreign APIs. Callback adapters must return cancellation or removal logic. Interruption can end the Effect without stopping a foreign operation that ignores cancellation; define settlement and cleanup honestly. For response bodies and async iterators, use [Lifetimes](LIFETIMES.md#runtime-and-stream-boundaries).

Transport handlers map expected errors to deliberate status/payload contracts. Keep secrets and internal exception payloads out of public responses. Report defects at the responsible owner instead of turning every failure into an ordinary client error.

Evidence: [HTTP client examples](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/50_http-client), [tryPromise](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Effect.ts). For cancellation across a Promise host and response body, read [OpenCode cancellation and settlement](OPENCODE_HOST.md#cancellation-and-settlement).

## Configuration Is Construction Input

Read runtime configuration through `Config` and provider layers at construction. Pass decoded configuration or acquire a configuration service in workflows; keep ambient environment reads out of domain logic. Use `Context.Reference` for defaultable settings, and required tags for authority such as credentials, persistence, or transport.

Use `Config.Redacted` for credentials and schema-based config for refined values. `withDefault` supplies missing-data defaults; malformed values still fail. Use an alternative provider or broad fallback only when accepting its failure behavior is deliberate.

Tests can provide `ConfigProvider.fromUnknown` through a provider Layer when exercising decoding, or supply the decoded configuration service directly. A library may offer concrete options plus a config-backed layer when both are useful consumer contracts.

Evidence: [Config](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Config.ts), [ConfigProvider](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/ConfigProvider.ts), [default references](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/03_services/10_reference.ts).
