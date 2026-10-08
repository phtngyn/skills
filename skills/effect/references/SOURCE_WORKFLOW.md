# Source Workflow

Use this guide when locating evidence, resolving version conflicts, or exploring an unfamiliar Effect feature. The common working loop lives in [SKILL.md](../SKILL.md).

## Locate And Compare

Resolve the installed package from the package containing the changed code; a workspace can contain several versions. Inspect its package metadata, lockfile entry, public exports, and relevant declarations or shipped source.

For a new project without an installed package, establish the intended version before choosing examples and verify against the installed package once available. For an existing v3 project, use matching v3 evidence; applying this v4 guide does not authorize a migration.

Use the first suitable local checkout: an explicit task/project pointer, `repos/effect` under the project or a nearby ancestor, or `../../repos/effect` relative to the real skill directory. Check candidates for `packages/effect/package.json` and `packages/effect/src`. Follow an explicitly documented alternative layout. Bound discovery to these locations instead of scanning the machine.

Inspect the checkout's HEAD and working status without modifying it. Dirty source is evidence from those exact contents, not simply from HEAD. A matching version is a useful filter; unreleased commits can retain the released version number. Verify relevant signatures and behavior against the installed package. Use a known matching ref through read-only Git inspection when available; preserve the checkout.

When sources disagree, the consuming project's instructions establish its conventions and the installed package establishes its available API. Compatible upstream examples and tests explain usage and semantics. This skill's summaries are revisable hypotheses. A newer checkout can suggest an approach but cannot establish compatibility by itself.

If no matching local evidence exists, use version-matched official documentation or source. Report the gap when it affects confidence. Fetching, upgrading, or switching the reference checkout is a separate maintenance action.

## Retrieve The Smallest Useful Evidence

Start with an exact symbol and the domain concept in `LLMS.md` or `ai-docs/src`. Read the matching example or section, not the complete generated document. Inspect `packages/effect/package.json` for the public import path and the owning source declaration for parameters, overloads, error types, requirements, and stability.

If the docs search finds no matching example, continue to the exported declaration and focused tests. Missing documentation does not establish that the API is absent.

For example, after setting `effect_repo` to the discovered checkout:

```sh
rg -n 'LayerMap|dynamic resources' "$effect_repo/LLMS.md" "$effect_repo/ai-docs/src"
rg -n '^export (const|class|interface).*Service|idleTimeToLive' "$effect_repo/packages/effect/src/LayerMap.ts"
rg --files "$effect_repo/packages/effect/test" | rg '/LayerMap\.'
```

Inspect the public implementation and follow internal calls only as far as the open question requires. Read focused tests for operational details such as cancellation, memoization, expiry, finalizer ordering, and failure propagation. A comment naming an API does not prove that the API is exported; a type signature alone does not prove runtime semantics.

For an uncertain call shape or type interaction, compile a minimal consumer expression with the target project's compiler. For uncertain behavior, run a focused test or disposable probe against its installed package. Point package-manager probes at the installed package or a disposable copy; local file links can write dependencies into the reference checkout. Keep generated artifacts outside reference checkouts and remove task-local probes when finished unless they become useful regression coverage.

Retain the source path, relevant finding, and compatibility basis in working context. Refresh that evidence only when the task crosses a new API/pattern or contradicts the finding. A routine task needs no separate evidence ledger.

## Find The Existing Mechanism

Paths below are relative to the discovered checkout at the extraction revision; bare module filenames refer to `packages/effect/src`. Confirm them with `rg --files` when the checkout differs. Use names as search terms; obtain actual imports from the installed export map.

| Need | Starting evidence |
| --- | --- |
| Services and layer composition | `ai-docs/src/01_effect/03_services`; `Context.ts`, `Layer.ts` |
| Resource ownership and framework integration | `ai-docs/src/01_effect/05_resources`, `ai-docs/src/04_integration`; `Scope.ts`, `ManagedRuntime.ts`, `LayerMap.ts` |
| Coordination and state | `Ref.ts`, `SynchronizedRef.ts`, `Semaphore.ts`, `Deferred.ts`, `Queue.ts`, `PubSub.ts`, `FiberMap.ts` and corresponding tests |
| Scheduling, deadlines, and calendar recurrence | `ai-docs/src/06_schedule`; `Schedule.ts`, `Cron.ts`, `DateTime.ts` |
| Result caching, scoped resources, and batching | `Cache.ts`, `ScopedCache.ts`; `ai-docs/src/05_batching`, `RequestResolver.ts` |
| Streams and backpressure | `ai-docs/src/03_stream`; `Stream.ts`, focused `Channel.ts`/`Sink.ts` operations |
| SQL, models, migrations, and transactions | `ai-docs/src/40_sql`; `packages/effect/src/sql`, installed driver under `packages/sql` |
| HTTP clients and typed servers | `ai-docs/src/50_http-client`, `ai-docs/src/51_http-server`; `packages/effect/src/http`, `packages/effect/src/http-api` |
| RPC and distributed entities | `packages/effect/src/rpc`, `packages/effect/src/cluster`, `packages/effect/src/workflow`; `ai-docs/src/80_cluster` |
| Reactive state and framework bindings | `packages/effect/src/reactivity`, `packages/atom`; search `Atom`, `AtomRuntime` |
| CLI and child processes | `ai-docs/src/70_cli`, `ai-docs/src/60_child-process`; `packages/effect/src/cli`, `packages/effect/src/process` |
| AI models, tools, and chat | `ai-docs/src/71_ai`; `packages/effect/src/ai`, installed provider under `packages/ai` |
| File systems, paths, sockets, and workers | Search `FileSystem`, `Path`, `Socket`, `Worker`; inspect `packages/platform` and installed host adapters |
| Observability and time | `ai-docs/src/08_observability`, `ai-docs/src/07_datetime`; `Metric.ts`, `DateTime.ts`, `packages/effect/src/observability` |
| Runtime and compiler tests | `ai-docs/src/09_testing`; `packages/effect/test`, `packages/effect/typetest`, `packages/vitest` |

Select by required semantics: a keyed result cache, resource cache, fiber registry, and durable workflow solve different contracts. Read their relevant behavior before choosing or building a substitute.

## Contributing To Effect Itself

When the target is the Effect monorepo, read its current `.agents/AGENTS.md` and relevant `.agents/skills` branches. They own repository-specific validation, generated barrels, JSDoc, migration generation, and package registration. Copying its command names into an unrelated application does not establish that application's checks.

Canonical extraction sources: `.agents/skills/effect-development/SKILL.md`, `.agents/skills/test-development/SKILL.md`, `.agents/AGENTS.md`, `LLMS.md`, and the package export map. See [provenance](../PROVENANCE.md).
