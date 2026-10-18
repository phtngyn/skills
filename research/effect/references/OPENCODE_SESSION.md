# OpenCode v2: Session Execution

Read this study when designing a shared executor, deciding whether concurrent callers join or queue, or separating process ownership from tenant/location capabilities. Revision and verification status are in the [study index](OPENCODE.md).

## Trace A Prompt

The concrete action is a user submitting a prompt while the same session may already be running. Recording the prompt and completing its execution have separate caller contracts.

1. The [HTTP handler](/Users/phtngyn/Developer/skills/repos/opencode/packages/server/src/handlers/session.ts:307) passes the payload to the public [Session service](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session.ts:416). The service selects a session handle; it does not construct a runtime for the request.
2. [Session.make and prompt](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/session.ts:38) capture host dependencies once, then reload current session state on each operation. `prompt` reconciles an existing message ID before preparing a new payload. [Preparation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/prompt.ts:32) borrows the selected instance, awaits plugin readiness, invokes hooks, and materializes attachments. Preparation is restored to interruptibility inside the admission workflow's mask.
3. [Admission](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/inbox.ts:155) records an inbox event. [Session.prompt](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/session.ts:145) then wakes execution unless `resume` is false, and returns the admitted item. Its response acknowledges recording; model completion is observed separately.
4. The global [SessionExecution layer](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/execution.ts:57) owns the coordinator. For each drain it reloads the session, selects the instance, and calls `SessionRunner.drain`. `Moved` and `Reloaded` results repeat selection with continuation data rather than permanently retaining the previous location's runner.
5. The location [runner implementation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/runner/llm.ts:38) drains eligible recorded work using its captured capabilities. Once the busy period ends, execution publishes a terminal event before resolving joiners. The event's local commit hook changes the execution claim in the same [projection transaction](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/bus.ts:317).

## Put Each Owner At The Right Boundary

| Boundary | What it owns or borrows | Why it exists |
| --- | --- | --- |
| Host Session capability | Stable store, inbox, execution and instance dependencies | Handles share implementations while reading current state by ID |
| Global SessionExecution | Per-session execution records and scoped fibers | One process coordinates a session across location handoffs |
| Instance selector | A location graph borrowed for the operation | A global service can route to a shorter-lived graph without capturing its runner permanently |
| Location SessionRunner | Model, plugin, lifecycle and other location capabilities | Location-specific dependencies are acquired with their owner |
| Durable store and event transaction | Recorded input and execution claims | Process-local fiber state cannot establish recovery after process death |

The [Instance contract](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/instance/service.ts) is separate from cache policy. Its [location-map implementation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/location-services.ts:74) supplies the borrowed graph through `Effect.provide(map.get(session.location))`. The runner's [contract](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/runner/index.ts) and substantial implementation are also separate. These are useful capability boundaries; a session handle and a pure terminal classifier do not each need another service tag.

## Choose The Competition And Stop Contracts

The [coordinator](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/run-coordinator.ts) keeps one execution record per key and uses a scoped `FiberSet` runtime for owned work. Its pending wake is a signal to inspect recorded work again; the durable inbox carries the commands.

| Operation | Observable contract |
| --- | --- |
| `run` | Start while idle, otherwise join the current execution's exit; a stopping execution settles before a fresh run starts |
| `wake` | Start while idle, otherwise request another drain; repeated wakes coalesce |
| `interrupt` | Clear previously accepted wakes and acknowledge interruption before finalizers finish |
| `interrupt` with `awaitSettlement` | Also wait for the execution captured by that call, including its settled hook |
| `awaitIdle` | Follow successor executions until the key has no owner |

A joined waiter's cancellation leaves the owned execution running. A wake during interruption cleanup is a new admission and starts a successor after cleanup. A wake after the final drain's eligibility check is also retained through settlement. These choices close concrete gaps between suspended work and the idle transition. Replacing a fiber on every wake would change the contract; serializing every wake as a command would also change it.

## Failure And Recovery

The execution service preserves typed runner failures for `resume` callers and classifies the terminal `Exit` for events. Success and ordinary failure release the claim. User/inactivity interruption releases it; owner-scope shutdown preserves it for restart. Lifecycle publication failures are reported by the owner rather than silently becoming successful domain execution. See [execution policy](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/execution.ts:50).

[SessionRestart](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/execution/restart.ts:23) finds claims left by dead processes, counts attempts durably before resuming, and terminalizes exhausted turns. Its contract explicitly assumes the previous owner is dead. Recovery is at least once: local serialization does not prevent repeating an external side effect after a crash. Adopt durable claims only when restart continuity is required, with an owner-election and idempotency policy appropriate to the application.

## Regression Evidence

These upstream tests were read, not executed. The gates and assertions establish the intended contracts independently of the coordinator's internal map.

| Contract | Test and observable assertion |
| --- | --- |
| Join same-key work | [Concurrent resumes](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-run-coordinator.test.ts:10): gate the drain, join two callers, observe one run |
| Coalesce without dropping recorded intent | [Wakes during execution](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-run-coordinator.test.ts:161): burst produces one follow-up; a wake during that follow-up produces another drain |
| Preserve work admitted during cleanup | [Wake during interruption cleanup](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-run-coordinator.test.ts:317): block cleanup, wake, release it, observe a new execution |
| Separate waiter and owner cancellation | [Interrupted joiner](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-run-coordinator.test.ts:504): cancel one waiter; the other completes after the single drain is released |
| Acknowledge before settlement | [Gated finalizer](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-run-coordinator.test.ts:602): stop returns while active ownership remains; `awaitIdle` observes cleanup completion |
| Distinguish completion, user stop and shutdown | [Execution claims](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-execution.test.ts:75): inspect database claims during execution and after each terminal path |
| Bound restart attempts | [Exhausted recovery](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/session-execution.test.ts:291): no drain starts; terminal failure releases the claim and resets accounting |

The selected tests do not directly isolate `awaitSettlement` following exactly one generation; that distinction is supported by implementation review. Add that acceptance case when exposing both settlement and idle waiting in another application.

## Apply The Reasoning

For a shared worker, choose its execution owner and same-key policy first. A service Layer can construct a shared owner and its fibers. Introduce an instance selector when operations cross owners, and a wake signal when the work itself is retained elsewhere. Derive tests from the caller promises before choosing a coordinator. General mechanisms live in [Architecture](../../../skills/effect/references/ARCHITECTURE.md), [Lifetimes](../../../skills/effect/references/LIFETIMES.md), and [Concurrency](../../../skills/effect/references/CONCURRENCY.md).
