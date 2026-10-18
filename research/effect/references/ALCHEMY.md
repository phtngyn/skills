# Alchemy Application Example

Alchemy illustrates capability-driven infrastructure wiring, reconciliation after partial failure, phased dependency readiness, and execution-owned resources. This study uses the [local source](/Users/phtngyn/Developer/skills/repos/alchemy) at `9e3c0584342d67b24a4215f931047aabd230327b`, reviewed on 2026-10-18. Its [workspace catalog](/Users/phtngyn/Developer/skills/repos/alchemy/pnpm-workspace.yaml) declares `effect: ^4.0.0` and overrides it to 4.0.4. Resolve APIs against the consuming project's declarations.

Use this example when an operation constructs a runtime capability, converges external state, exposes several readiness phases, or acquires resources lazily inside a longer-lived host. The [application index](APPLICATIONS.md) also routes OpenCode v2 and T3 Code by the guarantee required.

## Separate Capability Setup From Invocation

Trace the R2 read capability:

1. [ReadBucket](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Cloudflare/R2/ReadBucket.ts) describes binding a bucket to a typed client. Setup requires the binding service; the client's methods retain `RuntimeContext` as a call-time requirement.
2. [ReadBucketBinding](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Cloudflare/R2/ReadBucketBinding.ts) supplies the capability through `Layer.effect`. Its [shared builder](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Cloudflare/R2/BucketBinding.ts:22) captures the Worker environment and host during construction. At deploy time, calling the capability registers the bucket binding; the returned client performs runtime operations.
3. [Binding.Service](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Binding.ts:106) combines an Effect Context tag with a callable consumer API. Its explicit implementation resolves arguments and invokes the registered service. Effect's requirement type alone does not synthesize infrastructure or permissions.

The transferable design is to acquire stable adapter dependencies during construction while preserving requirements supplied by the invocation owner. A phase-specific requirement can reject calls from the wrong consumer context, provided the runtime bridge actually supplies that context. It is a type contract, not a security boundary.

Read, write and combined clients express different caller capabilities. Inspect the backend before inferring enforcement: the native R2 binding still exposes `raw`, and its deployment binding does not itself grant distinct read-only permissions. Restricted HTTP tokens have a different authority contract. Likewise, alternate adapters need a shared observable contract, not merely assignable interfaces. Alchemy's [R2 binding suite](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/Cloudflare/R2/Binding.test.ts) drives native and HTTP implementations through deployed Workers and explicitly treats multipart support as an adapter difference.

Use an ordinary service and Layer unless the consumer API needs Alchemy's combined callable/tag protocol or its deploy/runtime phases.

## Reconcile Observed State After Partial Failure

The engine cannot atomically commit a cloud mutation and its local checkpoint. [Apply's create path](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Apply.ts:752) persists a `creating` state and stable instance identity before provisioning, resolves dependency outputs and bindings, invokes the provider, then persists terminal attributes and the resolved binding payload. Recovery must account for mutations that happened before a failed or interrupted state write.

The [R2 bucket reconciler](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Cloudflare/R2/Bucket.ts:1253) shows the provider side:

- Observe the bucket using its stable physical name; a missing bucket becomes absence.
- Ensure existence. If a concurrent or earlier create produced `BucketAlreadyExists`, re-read it, with a bounded consistency retry for `NoSuchBucket`.
- Compare observed storage class with desired storage class and patch only the delta. Previously recorded properties cannot establish the current cloud value.
- Reconcile the remaining managed aspects and return attributes for the engine to persist.

This supports create, update, adoption and recreation through an observed-versus-desired flow. It does not make external operations exactly-once. Stable identity, ownership checks and provider-specific recovery still matter. Observation alone does not authorize adopting a foreign resource; Apply checks `Unowned` results before passing adopted attributes to reconciliation.

Apply this to resumable provisioning or synchronization when external state can drift or an external success can outlive a failed checkpoint. Treat each step's repeatability, read-after-write lag, ownership and managed fields explicitly. Retry the failure that is transient for this operation; a conflict or missing object is not universally recoverable. Ordinary unchanged plans may skip the provider entirely: Alchemy's separate drift workflow detects and repairs out-of-band changes.

## Distinguish Identity From Completed Readiness

Some resource cycles need a precreated identifier before their final configuration can be wired. [Apply](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Apply.ts:310) therefore maintains two `Deferred`s per node: an early output signal and a post-reconciliation signal. Only cycle peers use the early signal to break a dependency deadlock; ordinary downstream consumers wait for completed reconciliation. The later convergence pass brings cyclic bindings to final values.

The failure path completes both signals with the upstream Cause. Resolving an early identifier must not let an ordinary consumer report success after its upstream fails. Actions also wait for stable dependency outputs.

The general lesson is to name readiness by the fact it establishes. An identifier, listening socket, accepted request or placeholder can exist before a capability is usable. Give consumers the phase they require and settle every waiter on failure or cancellation. Add separate gates only when the workflow has distinct observable phases; Alchemy's cycle machinery is specific to its resource graph.

## Key Lazy Acquisition And Release To The Same Scope

A host can retain service descriptions longer than its platform permits retaining live I/O. Alchemy's [Worker bridge](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Cloudflare/Workers/WorkerBridge.ts:65) supplies a fresh event scope while reusing isolate-level construction. Its isolate scope has no normal teardown hook. Resource ownership must therefore follow the event or stream that actually uses the resource.

[makeExecutionMemo](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Runtime/ExecutionMemo.ts:37) allocates a symbol per memo construction and stores cached build Effects by the current Scope object. First access installs one memo before evaluating its build; concurrent callers share the pending acquisition. `Scope.provide(scope)` makes the resource's finalizer attach to the same scope used as the cache key. A different scope gets another acquisition, including after a failed build. [Drizzle.Postgres](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/src/Drizzle/Postgres.ts) uses this to defer connection setup until a query runs.

This is useful when runtime services survive multiple executions but sockets or pools must belong to one execution. Memoizing by request ID while acquiring in an ambient host scope can disagree about lifetime; using the actual owner scope keeps the two aligned. Nested scopes narrow sharing and release together.

The helper erases its `Scope` requirement because Alchemy's bridges promise to provide one. A general-purpose reusable API should retain that requirement unless its host supplies an equally explicit guarantee. Its failed build remains cached within the same scope; a new scope permits another attempt. Do not copy the WeakMap or failure-retention policy when ordinary scoped Layer composition already supplies the required sharing.

## Regression Evidence And Executed Checks

The following upstream cases were inspected:

| Contract | Evidence |
| --- | --- |
| Observed drift and recreation | [R2 Bucket.test.ts:706](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/Cloudflare/R2/Bucket.test.ts:706) changes storage class out of band and verifies repair; the following case deletes a bucket and verifies recreation with the same instance ID |
| Persist the values actually applied | [apply.test.ts:808](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/apply.test.ts:808) checks resolved binding payloads; the following redeploy case checks binding noops |
| Stable readiness | [apply.test.ts:1591](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/apply.test.ts:1591) observes that a downstream outside a cycle starts after reconciliation; [failure cases](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/apply.test.ts:1815) prevent downstream success and verify recovery |
| Interrupted generations | [apply.test.ts:6172](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/apply.test.ts:6172) gates replacement before create, after create and after reconciliation; interruption followed by destroy drains physical generations and state |
| Execution ownership | [ExecutionMemo.test.ts](/Users/phtngyn/Developer/skills/repos/alchemy/packages/alchemy/test/Runtime/ExecutionMemo.test.ts) checks per-scope sharing/release, concurrent joining, distinct memo cells, Layer finalizers and a fresh-scope retry after build failure |

All five ExecutionMemo cases passed in an isolated temporary workspace on Node 24.21.0, Effect 4.0.4, `@effect/vitest` 4.0.4 and Vitest 5.0.4. The implementation was copied unchanged. Only test-runner imports, the source import path and runner-specific suite tags were adapted. This verifies the memo helper, not the deployed bridges or database integration. The apply and live-cloud suites were read, not executed. No Alchemy dependencies, submodules or cloud resources were installed or provisioned in its checkout.

## Maintenance

Fetch `main` separately with `git -C repos/alchemy fetch origin main`, preserving the adopted checkout. Compare relevant implementation and tests before advancing the revision in UPSTREAM.md and provenance. Local source links follow the checkout. No Alchemy workspace installation is needed to use this study.
