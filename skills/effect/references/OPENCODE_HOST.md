# OpenCode v2: Embedded Host And Foreign Adapters

Read this study for a Promise-facing application host, a scoped SDK, or a streaming adapter whose resource use continues after its creating call resolves. Revision and verification status are in the [study index](OPENCODE.md).

## Trace Startup, A Request, And Close

The concrete action is creating an embedded client, opening an event stream, and closing the host while that stream is still active.

1. [EmbeddedHost.create](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/src/internal/host.ts:34) composes the router/application graph and logging into a `ManagedRuntime`. It awaits `contextEffect`, seeds host plugins, starts restart recovery through that runtime, and builds a web handler from the acquired context.
2. If startup fails after runtime creation, `onError` disposes the partially acquired runtime. Successful startup returns a host with an owned fetch transport and a close operation. Recovery runs in the runtime's lifetime rather than delaying startup until every recovered session completes.
3. The [Promise facade](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/src/promise.ts:42) executes acquisition at the foreign boundary, creates the client with `host.fetch`, and exposes `close`/`Symbol.asyncDispose`. The [Effect facade](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/src/effect/opencode.ts:42) instead uses `acquireRelease` so its caller's Scope closes the host. Its service Layer delegates to that same scoped acquisition.
4. [OwnedFetch](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/src/internal/fetch.ts:3) creates an AbortController and settlement Promise for each accepted request, forwards the caller's abort signal, and wraps the returned response body. Receiving response headers does not release the request record.
5. Host close immediately stops admission, shares one close Promise among callers, aborts active requests, awaits their settlement, then disposes the runtime. [Body tracking](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/src/internal/fetch.ts:65) releases the record on exhaustion, read failure, cancellation or abort cleanup.

## Match Each Lifetime

| Owner | Owned work or resource |
| --- | --- |
| Embedded host | ManagedRuntime, application graph and recovery fibers |
| Promise consumer or Effect caller Scope | Host close responsibility |
| Fetch request record | Handler settlement, caller abort listener and response-body consumption |
| Plugin activation scope | Registrations and foreign iterator cleanup installed by plugin setup |
| Individual API/tool invocation | Its execution and supported cancellation signal |

The [Effect client binding](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/src/effect/opencode.ts:47) supplies `FetchHttpClient.Fetch` during response execution. Fetch is read at request time, so providing it only during construction would let an ambient caller transport redirect embedded requests. Dependency capture must reach the point where the capability is actually used.

## Cancellation And Settlement

OwnedFetch separates prompt rejection from cleanup completion. `rejectOnAbort` can reject the caller's Promise before the handler settles; the rejection path retains the request record until the underlying handler does settle. For an open body, abort errors the outward stream and waits for the underlying reader's cancellation before releasing the record. The close operation joins those records before runtime disposal.

This is a cooperative contract. A handler or reader cancellation that never settles can keep close pending. Wrapping a Promise in cancellation does not make its foreign resource disappear. Decide whether the host promises to join cleanup, enforce a deadline, or report incomplete shutdown; test the promise chosen by the application.

## Plugin Context, Iterators, And Representation

The plugin [Promise adapter](/Users/phtngyn/Developer/skills/repos/opencode/packages/plugin/src/promise/adapter.ts:240) captures the activation's Effect context. Registrations run with that subscriber Scope; early disposal executes in the same context. Tool execution passes the invocation signal through the bridge. This belongs at the foreign API boundary, while domain services continue to return Effects.

[makeStreams](/Users/phtngyn/Developer/skills/repos/opencode/packages/plugin/src/promise/adapter.ts:45) wraps `Stream.toAsyncIterableWith`, tracks active iterator closers, and removes them on exhaustion, failure or early return. A plugin-scope finalizer calls each remaining iterator's `return`; the iterator's own scope and the subscriber's unload responsibility are separate. Optional abort signals close supported subscriptions.

[Endpoint adaptation](/Users/phtngyn/Developer/skills/repos/opencode/packages/plugin/src/promise/adapter.ts:166) derives input decoders and output encoders from protocol schemas. `adaptApiMethod` normalizes input through JSON, decodes it, calls the Effect operation, and encodes the result; no-content endpoints return undefined. An in-process Promise facade can still promise an encoded client representation. Exporting the decoded internal result directly would change that contract.

## Regression Evidence

These upstream tests were read, not executed.

| Contract | Test and observable assertion |
| --- | --- |
| Bind the owned transport during execution | [Transport tests](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/test/transport.test.ts:10): both acquisition and Layer clients use the embedded transport; the hostile ambient Fetch records no calls and remains in the caller context |
| Release completed and failed requests | [Request retention](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/test/request-retention.test.ts:11): repeated calls while the host remains open do not retain growing Request populations |
| Wire caller abort and host close | [Active requests](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/test/request-retention.test.ts:66): handler observes both abort causes; close disposes the handler |
| Cancel a body after headers resolved | [Open response body](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/test/request-retention.test.ts:104): pending read fails with the host-close reason and underlying body cancellation runs |
| Expose Promise stream cancellation | [Promise SDK](/Users/phtngyn/Developer/skills/repos/opencode/packages/sdk/test/promise.test.ts:36): caller abort and host close reject a pending event read |
| Preserve tool interruption across Promises | [Promise tool](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin/promise-tool.test.ts:15): interrupt the Effect fiber; the foreign executor's signal aborts and its Exit remains interruption |
| Normalize the Promise input contract | [Explicit undefined input](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin.test.ts:453): a Promise plugin can create a session with an explicitly undefined optional field through the JSON normalization path |

Separately, six [isolated transport checks](../PROVENANCE.md#opencode-validation) were executed against unmodified `OwnedFetch`, including gated body cancellation and handler settlement before disposal. They cover the transport without booting the application graph.

Startup disposal, plugin iterator unload and output encoding are supported here by implementation review; the selected tests do not independently prove those paths. For another host, add controlled startup failure, early iterator return/unload and schema round-trip cases to the relevant acceptance tests. Use [Testing](TESTING.md#control-the-interleaving) to keep those checks observable.

## Apply The Reasoning

For a conventional Promise framework, one host-owned ManagedRuntime and a close operation can be sufficient. Add active-call tracking when close must wait for foreign work or streaming bodies. Bind request context and cancellation at the invocation boundary; bind registrations to the subscriber. Specify the outward representation before writing adapters. General rules live in [Boundaries](BOUNDARIES.md#foreign-and-transport-adapters) and [Lifetimes](LIFETIMES.md#runtime-and-stream-boundaries).
