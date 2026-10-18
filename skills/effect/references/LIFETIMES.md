# Lifetimes

## Match Acquisition To Ownership

Choose the process, request, component, subscriber, operation or test that owns a resource. Acquire it there and register its real release action. Return scoped acquisition when callers choose the lifetime; use a Layer when service construction is the owner.

`acquireRelease` registers cleanup in a Scope; `acquireUseRelease` brackets one operation; `ensuring` attaches cleanup to an operation. Close explicit scopes at their owner. Acquisition protection prevents success from escaping before release is registered, but blocking acquisition still needs an appropriate interruption and foreign-cancellation contract.

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

A listener registry can outlive its subscribers. Registration ownership and callback invocation ownership are separate decisions. Layer acquisition should finish; start long-lived work in an owned fiber and give its later failures an explicit policy.

## Sharing And Keyed Graphs

Layer sharing depends on Layer identity and the relevant memo map. Reuse named Layers at a common owner. Equal options in repeated factory calls do not imply shared acquisition. Enclosing provision can reuse an existing build, while independent sibling builds need an explicit sharing policy. Use `Layer.fresh` or local provision when isolation is intentional; verify release-specific memoization semantics when the design depends on them.

Sharing a database does not share process-local wakeups, caches or cancellation signals. Share the implementation instance when its protocol depends on those signals.

Use ordinary scoped composition for one owner and keyed resource mechanisms such as `LayerMap` or `RcMap` when callers borrow independent keyed resources. Define identity, authority, idle retention, failed acquisition, invalidation and active-borrower behavior. Routing replacement and active-work cancellation are separate contracts. Guard delayed cleanup by generation identity when it could remove a replacement.

For lazy acquisition inside a shared host, align cache identity with the Scope that owns release. Some platforms permit shared service descriptions while restricting live I/O to one execution. Retain the Scope requirement on reusable APIs unless their host explicitly guarantees it.

## Runtime And Stream Boundaries

Use the platform's `runMain` at a process entrypoint or `Layer.launch` for Layer-owned application work. In a Promise framework, construct a `ManagedRuntime` at the host owner, reuse it across handlers and dispose it on shutdown. Clean up a partially constructed host when startup fails.

Choose application and invocation scopes separately. A runtime per request reacquires application resources; a process-wide runtime can retain resources beyond a test, tenant or reload owner.

Closing can begin before finalizers finish. If a host promises shutdown settlement, share and await its owned closing operation; do not infer settlement from repeated close or dispose calls. Avoid shutdown cycles in which owned work waits for the shutdown operation that must first join that work.

Streaming responses and async iterators stay active through consumption. Account for exhaustion, early return, read failure and abort. Keep their resources alive until that boundary settles. Stop admission, cancel or drain active work, await required cleanup, then dispose the host. State whether cancellation acknowledges a stop request or waits for cleanup.
