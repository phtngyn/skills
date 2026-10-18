# Lifetimes

## Match Acquisition To Ownership

Choose the process, request, component, subscriber, operation or test that owns a resource. Acquire it there and register the actual release action. Return a scoped acquisition when callers must choose the lifetime; construct a Layer when the service's lifetime is the right owner.

Use `acquireRelease` for a scoped resource, `acquireUseRelease` for one bracketed operation, and `addFinalizer` for cleanup in an existing scope. `ensuring` attaches cleanup to an operation rather than the lifetime of an acquired service. Close explicit scopes at their owner.

`acquireRelease` protects acquisition by default so success cannot leave an unregistered resource. For blocking acquisition, inspect its interruption option and the foreign API's cancellation behavior. Keep uninterruptible regions limited to transitions that must settle consistently; making the entire workflow uninterruptible can prevent shutdown.

Layer acquisition must finish. Start long-lived work in an owned fiber and return the acquired service. Define how later failures are joined, reported, or supervised using [Concurrency](CONCURRENCY.md#work-ownership).

Treat listeners, hooks, and registrations as resources too. The subscriber's scope should remove its entry; expose idempotent early disposal when callers need it. Make insertion and finalizer registration safe under interruption:

```ts
import { Effect } from "effect"

export const register = (
  listeners: Set<() => void>,
  callback: () => void,
) => Effect.acquireRelease(
  Effect.sync(() => {
    const entry = () => callback()
    listeners.add(entry)
    return { dispose: Effect.sync(() => { listeners.delete(entry) }) }
  }),
  (registration) => registration.dispose,
)
```

The registry can outlive individual subscribers. Callback invocation ownership is a separate decision from registration ownership. OpenCode v2's [registration study](OPENCODE_PLUGINS.md#separate-the-owners) supplies evidence for this distinction.

Evidence: [acquisition](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/05_resources/10_acquire-release.ts), [Effect resource primitives](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Effect.ts).

## Sharing And Keyed Graphs

Layer sharing depends on Layer identity and the relevant memo map/scope. An enclosing `Effect.provide` or runtime can supply an already-built Layer; sibling `provide` calls build separate copies even when given the same Layer value. Reuse named Layers at a common owner, or share an explicit memo map when separate runtimes must share acquisition. Equal options in repeated factory calls do not imply the same Layer identity. Use `Layer.fresh` or `provide`'s `local` option when isolation is intentional.

Storage identity and service identity are separate. Instances using the same database can own different process-local wakeups, cancellation signals or caches. Share the instance when its protocol depends on those signals, as in [T3 Code's outbox wiring](T3_CODE.md#keep-capabilities-reachable-across-transports). Persisted intent can outlive a process; its native handles and fibers still need process-owned lifetimes.

Separate dependencies whose owners differ. An application service may select and borrow a request, account or tenant capability for an operation; it must not retain that capability beyond its owner. Keys must include the identity and authority that determine safe sharing. Canonicalize equivalent keys before lookup and invalidation.

Reuse a shared Layer for one resource owner; use `LayerMap` when callers borrow independent keyed service graphs. Its underlying reference-counted ownership means invalidation detaches future lookup while existing borrowers can retain the old graph. Define these application policies separately:

- Retention: release when idle, keep until explicit invalidation, or evict according to application activity.
- Replacement: permit old borrowers to finish, or stop their work and await settlement before handoff.
- Failed acquisition: retain the failure or remove it so a later lookup can retry.

When build cleanup can overlap replacement, check generation identity before deleting the current entry. Avoid awaiting cleanup that waits for the same lookup or readiness transition; let an independent owner settle it when that contract requires it. These are dynamic-replacement concerns, not reasons to add a custom cache to every service.

Evidence: [Layer memoization](/Users/phtngyn/Developer/skills/repos/effect/migration/layer-memoization.md), [LayerMap](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/05_resources/30_layer-map.ts), [RcMap.invalidate](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/RcMap.ts), [OpenCode keyed graphs](OPENCODE.md#keyed-service-graphs). For result retention rather than resource lifetime, read [Operations](OPERATIONS.md#caching-and-batching).

OpenCode v2's [ownership map](OPENCODE_SESSION.md#put-each-owner-at-the-right-boundary) illustrates borrowing a shorter-lived capability from a long-lived service. Apply the ownership relationship using the consuming project's resource identities.

## Runtime And Stream Boundaries

Use the platform's `runMain` at a process entrypoint; use `Layer.launch` for an application whose work is owned by Layers. For a Promise-based framework, create a `ManagedRuntime` at the host owner, reuse it across handlers, pass the request AbortSignal when supported, and await disposal on shutdown. Translate expected failures into the framework's result contract before the Promise edge.

A runtime per request reacquires application resources. A global runtime is wrong when the actual owner is a test, account, or hot-reloaded host. Separate runtimes share acquisition only when an intentional memo-map policy connects them. If startup fails after runtime creation, dispose the partially constructed host.

Closing starts before cleanup finishes. A Scope enters its closed state when closing starts; another `Scope.close` returns immediately even while earlier finalizers run. A host that promises settlement must retain and await its closing operation. In the reviewed source, overlapping external `ManagedRuntime.dispose` / `disposeEffect` calls wait for disposal to finish. Runtime-owned fibers and finalizers that call disposal again do not wait for it, because disposal must interrupt or run them to finish.

An Effect-to-Promise facade must preserve the needed service context and deliberately assign scopes: long-lived registrations belong to their subscriber, while call resources belong to the invocation. Capturing a Scope in a context alone does not define the lifetime of every future operation.

Streaming responses and async iterators remain active after the creating Promise resolves. Track exhaustion, early return, failure, and abort; close underlying consumers and remove abort listeners. Shutdown stops admission, cancels or drains active work, awaits cleanup, then disposes the runtime. Define whether an interruption method acknowledges the stop request or waits for cleanup; expose a separate settlement operation when callers need both.

Evidence: [ManagedRuntime integration](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/04_integration/10_managed-runtime.ts), [disposal implementation](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/ManagedRuntime.ts), [Scope.close](/Users/phtngyn/Developer/skills/repos/effect/packages/effect/src/Scope.ts), [process entrypoints](/Users/phtngyn/Developer/skills/repos/effect/ai-docs/src/01_effect/06_running). For host construction and close during streaming consumption, read [OpenCode embedded host](OPENCODE_HOST.md#trace-startup-a-request-and-close).
