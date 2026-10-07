# Streams

## Mental Model

`Stream<A, E, R>` is an effectful source that can emit many `A` values over time, fail with `E`, and require services `R`. Streams are pull-based and backpressured; consumption controls demand.

For a repeated effect without emitted values, use [SCHEDULING.md](SCHEDULING.md).

## Source Chooser

- In-memory values: `Stream.make(...)` or `Stream.fromIterable(...)`.
- Test fixtures: `Stream.fromIterable(...)`, often with `Stream.concat(Stream.never)` for an open subscription.
- Queue-backed callback boundary: `Queue` plus `Stream.fromQueue(...)`.
- Broadcast events: `PubSub` plus `Stream.fromPubSub(...)`.
- Latest-value state plus updates: `SubscriptionRef`.
- Schedule-generated ticks/values: `Stream.fromSchedule(...)`.
- Paginated pull APIs: `Stream.paginate(...)`; its effectful step returns `Effect<readonly [ReadonlyArray<A>, Option<S>], E, R>`. The stream emits `A` elements, not page arrays. `Option.none()` ends pagination after emitting that step's elements; empty arrays are allowed.
- Async iterable/platform source: `Stream.fromAsyncIterable(...)` when no native Effect source exists.
- Effect that produces a stream after reading services/config: `Stream.unwrap(...)`.

## Transformation Chooser

- Pure transformation: `Stream.map(...)`.
- Effectful transformation: `Stream.mapEffect(...)`.
- Bounded concurrent effectful transformation: `Stream.mapEffect(fn, { concurrency })`.
- Drop ordering when order is irrelevant and latency matters: `Stream.mapEffect(fn, { concurrency, unordered: true })`.
- One input to zero/many outputs: `Stream.flatMap(...)`.
- Multiple inner streams concurrently: `Stream.flatMap(fn, { concurrency })`.
- Keep only matching values: `Stream.filter(...)` / `Stream.filterEffect(...)`.
- Stateful transformation: `Stream.mapAccum(...)` / `Stream.mapAccumEffect(...)`.

## Consumption Chooser

- Side-effecting consumer: `Stream.runForEach(...)`.
- Ignore elements but run the stream: `Stream.runDrain`.
- Tests/small finite streams: `Stream.runCollect`.
- First N values in tests: `Stream.take(n)` plus `Stream.runCollect`.
- Fold into a value: `Stream.runFold(...)`.
- Long-lived consumer in a layer: `stream.pipe(Stream.runForEach(...), Effect.forkScoped)`.

Avoid `Stream.runCollect` on unbounded or production event streams.

## Long-Lived Consumers

Own long-lived stream consumers in layers and fork them into the layer scope.

```ts
export const layer = Layer.effectDiscard(
  Effect.gen(function* () {
    const gateway = yield* Gateway

    yield* gateway.events.pipe(
      Stream.filter(isMessageEvent),
      Stream.runForEach(handleEvent),
      Effect.forkScoped,
    )
  }),
)
```

For lifetime and supervision, read [RESOURCES_RUNTIME.md](RESOURCES_RUNTIME.md) and [CONCURRENCY_STATE.md](CONCURRENCY_STATE.md).

## Queues, PubSub, And SubscriptionRef

Choose the producer primitive using [CONCURRENCY_STATE.md](CONCURRENCY_STATE.md). Expose streams to consumers and keep producer queues/private refs inside the implementation or test service.

Good service shape:

```ts
export interface Interface {
  readonly events: Stream.Stream<ProviderEvent, ProviderError>
  readonly status: Stream.Stream<ProviderStatus>
}
```

## Backpressure And Buffers

Prefer natural stream backpressure first.

Use `Stream.buffer(...)` only when producer and consumer should decouple.

- `strategy: "suspend"`: apply backpressure when full.
- `strategy: "dropping"`: drop new values when full.
- `strategy: "sliding"`: keep the latest values by dropping old ones.
- `capacity: "unbounded"`: rare; use only when growth is bounded elsewhere.

Use `Stream.debounce(...)` for quiet-period behavior and `Stream.throttle(...)` / `Stream.throttleEffect(...)` for rate-shaped streams.

## Recovery And Keyed Processing

Use `Stream.mapError` for translation and `catchIf`, `catchTag`, or `catchFilter` for typed recovery. Apply the failure policy in [ERRORS.md](ERRORS.md). For replacement, ordered groups, or coalesced reconciliation, use the chooser in [CONCURRENCY_STATE.md](CONCURRENCY_STATE.md).

## Tests

- Use `Stream.fromIterable(...)` for finite fixtures.
- Use `Stream.empty` for no events.
- Use `Stream.fromQueue(...)` with a test-owned `Queue` when the test needs to drive events interactively.
- Use `Stream.take(n)` plus `Stream.runCollect` for finite assertions.
For deterministic coordination and time, read [TESTING.md](TESTING.md).
