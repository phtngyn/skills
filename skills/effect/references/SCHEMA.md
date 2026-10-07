# Schema And Data Modeling

## Records

For plain records, this skill personally prefers `Schema.Struct(...)` plus a same-name `interface`. This is not an upstream restriction; Effect application examples also use class schemas.

```ts
export const User = Schema.Struct({
  id: UserId,
  name: Schema.NonEmptyString,
  email: Schema.optionalKey(Schema.String),
})

export interface User extends Schema.Schema.Type<typeof User> {}
```

Guidance:

- Add `.annotate({ identifier: "User" })` only when tooling consumes it: HTTP API, RPC, OpenAPI/JSON Schema, docs, diagnostics, or codegen.
- Use `schema.make(...)` when construction is trusted.
- Use `schema.makeEffect(...)` when construction failure should stay in the Effect error channel.
- Use `schema.makeOption(...)` when constructor validation details may be discarded.
- Decode unknown input at boundaries with `Schema.decodeUnknownEffect(...)` by default.
- Use `Schema.decodeUnknownSync(...)` only in scripts, tests, or startup paths where throwing is acceptable.
- Use `Schema.decodeUnknownOption(...)` only when mismatch details are intentionally discarded.
- Use `Schema.decodeUnknownResult(...)` for pure code that wants explicit success/failure without Effect.

### Construction Versus Decoding

`make` / `makeEffect` apply constructor defaults and type-side validation. They are
not decoders for an unknown encoded representation. For example, decode a wire
timestamp through its string-to-DateTime codec rather than passing the string to
the decoded value's constructor.

- `Schema.decodeUnknownEffect(schema)(input)` fails with `Schema.SchemaError`.
- `SchemaParser.decodeUnknownEffect(schema)(input)` exposes the raw `SchemaIssue.Issue` for low-level parser composition.
- `schema.makeEffect(input)` also exposes `SchemaIssue.Issue`; wrap it explicitly with `Effect.mapError((issue) => new Schema.SchemaError(issue))` if the boundary needs `SchemaError`.
- `schema.make(input)` throws a plain `Error` with the issue in `cause` on validation failure; do not assume it throws `SchemaError`.
- `Schema.NumberFromString` rejects empty/whitespace-only strings and trailing junk in v4. Do not depend on v3's `parseFloat`-style prefix parsing.

## Class Schemas

Use `Schema.Class` when a validated class constructor, instance methods, or class identity is useful. Use `Schema.TaggedClass` for the corresponding tagged model. They are supported application patterns; ordinary records do not need class identity merely because a schema exists.

```ts
import { Schema } from "effect"

export class UserProfile extends Schema.Class<UserProfile>("myapp/UserProfile")({
  name: Schema.NonEmptyString,
}) {
  get displayName(): string {
    return this.name
  }
}
```

Class construction is not unknown-wire decoding: keep the same boundary distinction as for structs. Follow an established project choice consistently.

## Field And Contract Reuse

Reuse fields directly when contracts are semantically related.

```ts
export const CreateUserInput = Schema.Struct({
  name: User.fields.name,
  email: User.fields.email,
})

export const StoredUser = User.pipe(
  Schema.fieldsAssign({
    createdAt: Schema.DateTimeUtcFromString,
  }),
)
```

Guidance:

- Use `.fields`, `Schema.fieldsAssign(...)`, and `.mapFields(...)` when contracts are genuinely related.
- Use `Schema.encodeKeys(...)` when decoded TypeScript names differ from encoded wire/storage keys and naming is the only difference.
- Keep explicit mapping when behavior, joins, validation, or domain translation is involved.
- Use `Schema.extendTo(...)` sparingly for decoded-only derived fields.
- Use field reuse to build small related contracts, not one oversized inheritance-by-schema object.

## Optionality And Defaults

- Use `Schema.optionalKey(...)` for absent JSON/storage keys.
- Use `Schema.optional(...)` only when explicit `undefined` is part of the contract.
- Use `Schema.NullOr`, `Schema.UndefinedOr`, or `Schema.NullishOr` only when nullish values are truly part of the encoded contract.
- Keep normalized defaulted values as required fields and apply defaults in constructors/decoding.
- Do not make domain values optional merely for construction convenience.

## Nominal Values

- Use constrained branded schemas for scalar IDs and value objects.
- Use normal schema constraints before `Schema.brand(...)` for most code.
- Reach for `Schema.fromBrand(...)` only when the project already models brands with `Brand` constructors or wants the check packaged with the brand constructor.

## Variants

```ts
type Step = Data.TaggedEnum<{
  Continue: { readonly cursor: number }
  Finished: { readonly count: number }
}>

export const Step = Data.taggedEnum<Step>()

const next = Step.Continue({ cursor: 10 })
const label = Step.$match(next, {
  Continue: ({ cursor }) => `continue at ${cursor}`,
  Finished: ({ count }) => `finished ${count}`,
})
```

```ts
export const Event = Schema.TaggedUnion({
  Started: { runId: RunId },
  Finished: { runId: RunId, result: Schema.Json },
})

export type Event = typeof Event.Type

const event = Event.cases.Started.make({ runId })
const label = Event.match(event, {
  Started: ({ runId }) => `started ${runId}`,
  Finished: ({ runId }) => `finished ${runId}`,
})
```

Guidance:

- Use `Data.TaggedEnum` for internal control-flow algebras; it provides constructors, `$is`, and exhaustive `$match`. Do not add a Schema solely to obtain these utilities.
- Use `Schema.TaggedStruct` for the ordinary Effect-owned `_tag` variant.
- Use `Schema.TaggedUnion` when the union needs decoding, encoding, persistence, wire validation, JSON Schema derivation, or schema composition.
- Prefer a principled split over forcing one representation everywhere: Data internally, Schema at boundaries.
- Use `Schema.tag(...)` when an external contract has a custom discriminator field such as `type` or `kind`; combine those structs with `Schema.toTaggedUnion("type")` when union helpers are needed.
- If the encoded contract omits the discriminant, use `Schema.tagDefaultOmit(...)` deliberately.

## Errors

For error representation, reasons, translation, and interruption, read [ERRORS.md](ERRORS.md).
