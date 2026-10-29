# Source Lookup

## Establish The Release

For implementation or migration, verify the latest stable release from the package registry (`npm view effect dist-tags --json`, or the project's registry equivalent). Use the `latest` release rather than snapshot, beta or rc tags. Upgrade the project's declarations and lockfile with its package manager when needed, and choose compatible companion packages. Reuse that result during the task.

Check the resolved package and its public exports. A source checkout whose package.json declares the same version can contain unreleased commits; match a release tag or verify the source against the installed package before relying on implementation details.

Read the release changelog before upgrading, including intervening patches. Check each affected API's stability annotation: unstable and experimental APIs can change within a stable package release. Include persisted formats and wire protocols in the migration review; passing types do not establish compatibility with old data or peers.

## Look Up The Concrete Question

Use the project's Effect clone at `repo/effect` (or `repos/effect` where that layout is used). Match its revision to the selected release, then inspect `packages/effect/src`, focused tests and companion packages for the concrete question. Use the resolved package's declarations and included source to check the published surface. Keep reference sources read-only; use an isolated checkout if a different revision is needed.

Search the relevant symbol and inspect public declarations first. Read implementation and focused tests when types do not establish cancellation, sharing, failure retention, ordering or cleanup. If the release includes `LLMS.md` or `ai-docs`, use their index to find the relevant example. Do not load a full manual for a single API question.

Use a small compiling or executable probe for an uncertain overload or lifecycle guarantee. Reuse evidence until a new requirement or contradictory result calls for another lookup. An application's custom helpers and conventions do not establish Effect API behavior.

## Find The Mechanism

Paths below are relative to an Effect source checkout; published packages commonly include `src/` and declarations instead. Use supported public exports for application imports.

| Decision | Starting modules or examples |
| --- | --- |
| Construction and ownership | `Context`, `Layer`, `Scope`, `ManagedRuntime`, `LayerMap` |
| Coordination and state | `Ref`, `SynchronizedRef`, `Semaphore`, `Deferred`, `FiberMap`, `FiberSet` |
| Streams and delivery | `Stream`, `Queue`, `PubSub`, `SubscriptionRef` |
| Scheduling and reuse | `Schedule`, `Cache`, `ScopedCache`, `Request`, `RequestResolver` |
| Schemas and errors | `Schema`, `SchemaParser`, `Data`, `Cause`, `Exit` |
| Cryptography and platform provision | `crypto/` and the platform's crypto layers |
| File discovery and encoded streams | `Glob`, `FileSystem`, `encoding/` |
| HTTP, SQL, RPC and workflows | `http/`, `http-api/`, `sql/`, `rpc/`, `workflow/`, `cluster/` |
| Framework and platform features | `reactivity/`, `cli/`, `process/`, `ai/`, and compatible platform packages |
| Tests and consumer types | `testing/`, `test/`, `typetest/`, and `@effect/vitest` |

Check existing native mechanisms before adding custom infrastructure. Select by the required guarantee: result retention, resource ownership, joining work and durable recovery are distinct contracts. When contributing to Effect itself, read its contributor instructions for that work.
