# T3 Code Application Example

T3 Code illustrates shared Layers, durable command admission, worker recovery, publication ordering and replayable streams. This example uses the [local source](/Users/phtngyn/Developer/skills/repos/t3-code) at `2fbd4318fc5b610c3e7fcfcbd5bbd80b73521d8f`; its [dependency catalog](/Users/phtngyn/Developer/skills/repos/t3-code/pnpm-workspace.yaml) pins Effect and `@effect/vitest` to 4.0.5. Review dates and executed checks are recorded in [provenance](../PROVENANCE.md). Resolve APIs against the consuming project's declarations.

## Choose A Workflow

| Decision | Workflow |
| --- | --- |
| Share capabilities across entry points | [Service construction and Layer wiring](#keep-capabilities-reachable-across-transports) |
| Commit intent and execute external work | [Admission, cancellation and recovery](#separate-durable-acceptance-from-execution) |
| Keep live delivery in commit order | [Commit-to-publication handoff](#preserve-publication-order-explicitly) |
| Deliver stored history with live events | [Replay, retention and cleanup](#bound-the-whole-replay-and-live-pipeline) |

For dynamic resource replacement and Promise host ownership, see the [OpenCode v2 example](OPENCODE.md). The [shared index](APPLICATIONS.md) routes all three examples by the guarantee required.

## Keep Capabilities Reachable Across Transports

T3's [service conventions](/Users/phtngyn/Developer/skills/repos/t3-code/docs/internals/effect-services.md) put a feature behind a domain capability because WebSocket, MCP, scheduled tasks and CLI all need to reach it. Handlers decode, invoke and map errors. [runtimeLayer.ts](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/runtimeLayer.ts:72) composes ordinary Layers into shared stores, sink, executor and worker subgraphs. The sink and worker use the same outbox instance: its SQL rows are durable, but its wakeups and cancellation signals are process-local.

**Lesson:** place reusable behavior below its entry points. Capture stable dependencies at service construction and share stateful dependencies at the composition owner. Two instances pointing at the same database do not necessarily share notifications or cancellation. A small operation can still be a function; T3's service-per-server-capability rule, namespace imports, module ordering, schema-backed errors everywhere, and `catchTags` preference are local conventions.

Ordinary named Layers express this shared graph. OpenCode's [graph compiler](OPENCODE.md#composition-and-replacement) addresses transitive replacement and distinct sharing domains. Choose construction machinery from those requirements.

## Separate Durable Acceptance From Execution

Trace [EventSink.commitCommand](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EventSink.ts:559):

1. Reserve a command receipt inside the SQL transaction. A duplicate returns the existing receipt and events.
2. Append events, update projections, enqueue outbox work and finalize the receipt in that transaction. Optional cancellation of unsettled work participates in the commit.
3. After commit, signal cancellations, wake workers and publish stored events. No new work is enqueued for a duplicate receipt.
4. [EffectOutbox.claimNext](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EffectOutbox.ts:529) atomically selects and marks work running. [EffectWorker](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EffectWorker.ts:673) executes the external operation and settles its durable status separately.

**Lesson:** an accepted command promises committed intent; it does not promise the external operation finished. Persist authoritative state and required work together when a crash between them would lose the job. Wakeups accelerate discovery; persisted work permits recovery. Define receipt identity, execution identity and completion separately.

An outbox does not make an external operation exactly-once. Execution can succeed before settlement fails. T3 [classifies replay-safe versus process-bound effects](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EffectOutbox.ts:120), and its [post-success settlement policy](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EffectWorker.ts:663) requeues the former and attempts to terminalize the latter. Recovery also distinguishes these classes after process loss. These lists describe T3's provider contracts; determine replay safety for the current adapter, including ambiguous external outcomes and idempotency keys. Do not infer it from an Effect's type or from a lease alone.

For cancellation, claim registration creates a local Deferred, the worker arms its cancellation path before rereading the authoritative row, and then races execution against cancellation. This combines durable state with a local wakeup to cover the gap between claim and execution. It still relies on the external adapter's cancellation and settlement behavior.

Use this machinery only when the task requires durable work. A scoped fiber or bounded `forEach` is sufficient for many finite or process-owned workflows. Effect's durable workflow facilities are another option to assess through [Source lookup](../../../skills/effect/references/SOURCE.md).

## Preserve Publication Order Explicitly

[EventSink.commitThenPublish](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EventSink.ts:234) explains a race: writer A commits and is descheduled; B commits and publishes first. A client that has advanced its cursor to B may discard A's later notification.

The sink acquires a semaphore lane before leaving the transaction, retains it through publication and releases it with `ensuring`. This connects transaction order to live publication order for this sink. The semaphore alone is not a cross-process ordering protocol, and this design must be assessed against the database transaction/connection behavior.

**Lesson:** define whether ordering applies to deciding, committing, publishing, executing or acknowledging. A database transaction or per-key lock establishes only the boundary it actually protects. Prove the handoff when a downstream consumer uses monotonic cursors. Do not hold locks over arbitrary external I/O by default.

## Bound The Whole Replay And Live Pipeline

[EventSink.stream](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EventSink.ts:748) combines stored history with live notifications. The bounded RPC path delegates to [LiveStreamBudget](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/LiveStreamBudget.ts:279):

- Subscribe and begin draining live events before querying the high-water mark. Replay through that mark, then deliver live events above it; discard overlap.
- Filter irrelevant events and project wire payloads before retention. Charge retained item count and serialized bytes, including a delivered batch until the next pull acknowledges it.
- Bound the live tail while high-water queries, replay, downstream projection or acknowledgement are blocked. A bounded final queue cannot bound an earlier unbounded subscription by itself.
- On overflow, fail the stream with a resumable-cursor instruction, close the subscription and blocked source, and release pending data. Already delivered items remain charged until acknowledgement or scope closure.

**Lesson:** map every retention stage, including source chunks and in-flight delivery. Choose backpressure, dropping, coalescing or disconnect-and-resume from the delivery contract. Item count alone is insufficient when payload sizes vary substantially. Serialized-byte accounting is a useful budget, not an exact heap measurement. T3 retains unbounded internal subscriptions on other paths; the RPC budget is not a claim that every stream in the app is bounded.

Use durable replay only when consumers require it. A live PubSub, current-value subscription, work queue and replayable log have different guarantees.

## Regression Evidence And Executed Checks

The following focused tests were read; only the LiveStreamBudget suite was executed here.

| Contract | Source evidence and assertion |
| --- | --- |
| Idempotent admission | [FoundationPersistence.test.ts:1433](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/FoundationPersistence.test.ts:1433): duplicate receipt retains one outbox row; a subsequently constructed worker executes once |
| Cancellation registration gap | [EffectWorker.test.ts:306](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EffectWorker.test.ts:306): cancellation during the durable precheck causes zero execution and settlement calls |
| Success followed by settlement failure | [EffectWorker.test.ts:371](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/EffectWorker.test.ts:371): process-bound success terminalizes; the following replay-safe case requeues |
| Per-key execution | [FoundationPersistence.test.ts:2621](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/FoundationPersistence.test.ts:2621): gated first work blocks its successor while another thread starts |
| Commit/publication handoff | [FoundationPersistence.test.ts:3472](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/FoundationPersistence.test.ts:3472): gate the first writer after commit, start a second, then assert increasing published sequences |
| Replay, overflow and cleanup | [LiveStreamBudget.test.ts](/Users/phtngyn/Developer/skills/repos/t3-code/apps/server/src/orchestration-v2/LiveStreamBudget.test.ts): nine cases cover ACK retention, item/byte limits, blocked high-water/replay cleanup, replay/live overlap and blocked projection |

All nine LiveStreamBudget tests passed in an isolated temporary workspace on Node 24.21.0, Effect 4.0.5, `@effect/vitest` 4.0.5 and Vitest 5.0.4. The implementation was copied unchanged; the test's `vite-plus/test` import was changed to `vitest` to match the available runner. This validates the stream helper under that harness, not T3's patched Vite+ integration, real RPC acknowledgement, SQL transactions, worker recovery or full server. The source checkout remains unmodified.

## Refresh

Fetch `main` separately with `git -C repos/t3-code fetch origin main`, preserving the reviewed checkout. Compare changed implementation and tests before adopting another revision. Record adoption in UPSTREAM.md and provenance; local source links follow the checkout. No T3 workspace installation is needed to use the skill.
