# HTTP Clients

Import HTTP modules through `effect/http` or its supported leaf exports; see [V4_APIS.md](V4_APIS.md). Prefer Effect HttpClient when typed errors, layers, and transforms fit. Raw `fetch` is appropriate for platform transports, constrained runtimes, or libraries deliberately avoiding unstable HTTP APIs.

## Boundary Shape

HTTP adapter methods should be named effects that own the full boundary:

- construct request
- attach auth and headers
- execute request
- classify status
- decode response body
- map transport/status/decode failures to typed domain errors
- apply retry/rate-limit policy where idempotent

## Effect HttpClient

Useful APIs:

- `HttpClient.get(...)`, `post(...)`, `put(...)`, `patch(...)`, `del(...)`, `execute(...)` for service accessors.
- `HttpClient.mapRequest(...)` / `mapRequestEffect(...)` for configured client transforms.
- `HttpClientRequest.prependUrl(...)` for base URLs.
- `HttpClientRequest.bearerToken(...)` for bearer auth.
- `HttpClientRequest.acceptJson` for JSON accept headers.
- `HttpClientRequest.bodyJson(...)` for effectful JSON body encoding.
- `HttpClientRequest.schemaBodyJson(...)` for schema-backed JSON body encoding.
- `HttpClient.filterStatusOk` / `HttpClientResponse.filterStatusOk` before decoding when non-2xx responses are failures.
- `HttpClientResponse.schemaBodyJson(...)` for body-only decoding, `schemaJson(...)` for status/headers/body decoding, and `schemaNoBody(...)` for status/headers decoding.

## Retry And Rate Limits

`HttpClient.retryTransient` handles transport errors, timeouts, and statuses 408, 429, 500, 502, 503, and 504.

`HttpClient.withRateLimiter` paces requests and learns from rate-limit / `Retry-After` headers. It requires a `RateLimiter` plus initial window, limit, and key options, adds `RateLimiterError`, and retries 429 responses. Set `times` to bound retries (`0` disables them); the default is unlimited.

Use operation-level `Effect.retry(...)` when retry depends on domain-specific typed errors, provider payloads, or idempotency rules. Read `SCHEDULING.md` for custom schedules and `retryAfterMs` typed-provider patterns.

## Raw Fetch Adapter

Pass the `Effect.tryPromise` signal to `fetch`, classify status before decoding, and translate failures at the adapter boundary:

```ts
const request = Effect.fn("Provider.request")(function* (input: RequestInput) {
  const response = yield* Effect.tryPromise({
    try: (signal) => fetch(input.url, { signal, headers: input.headers }),
    catch: (cause) => new ProviderError({ operation: "Provider.request", cause }),
  })

  if (!response.ok) {
    return yield* Effect.fail(new ProviderRejected({
      operation: "Provider.request",
      status: response.status,
    }))
  }

  const json = yield* Effect.tryPromise({
    try: () => response.json(),
    catch: (cause) => new ProviderError({ operation: "Provider.decodeJson", cause }),
  })

  return yield* Schema.decodeUnknownEffect(ResponseSchema)(json).pipe(
    Effect.mapError((cause) =>
      new ProviderError({ operation: "Provider.decodeResponse", cause }),
    ),
  )
})
```

Preserve diagnostic evidence while redacting secrets and private payloads. Apply the retry policy in [SCHEDULING.md](SCHEDULING.md).
