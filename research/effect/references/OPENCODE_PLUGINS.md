# OpenCode v2: Plugin Reload And Readiness

Read this study for hot-reloaded subscribers, coalesced refreshes, readiness during replacement, or cleanup that can call back into its owner. Revision and verification status are in the [study index](OPENCODE.md).

## Trace A Change

The concrete action is a plugin file changing while initial activation or a previous reload is still in flight.

1. The location [supervisor Layer](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin/supervisor.ts:140) captures the registry, source resolver, module loader, update checker and event bus. It acquires an initial readiness hold and registers cleanup. Layer acquisition starts scoped consumers and returns; readiness has its own contract.
2. [Source consumers](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin/supervisor.ts:205) subscribe before activation. Each notification advances `observed`, acquires a hold if needed, and offers that number to `Queue.sliding(1)`. File, policy, host-plugin and periodic triggers share this path.
3. One sequential `Stream.runForEach` consumer runs initial activation immediately and debounces later triggers. [Activation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin/supervisor.ts:158) resolves available definitions, applies them to the registry, and then handles missing package installation. Intermediate notifications can be discarded because activation recomputes current desired state.
4. The [registry](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin.ts:89) holds readiness and serializes activation. It retains the unchanged prefix of ordered registrations, unloads the changed suffix in reverse order, and loads the new suffix. Plugin ordering affects state contributions, so replacement is more than swapping a map entry.
5. The supervisor releases its hold only when the completed target equals the latest observed notification. An update accepted during activation keeps readiness pending for the follow-up. Independently forked update checks use an activation generation guard before publishing their result.

The consumer is the serialization mechanism; debounce is the burst policy. The capacity-one queue is appropriate because notifications mean “recompute current state.” A queue of commands that must each execute needs a different retention contract.

## Separate The Owners

| Owner | Responsibility |
| --- | --- |
| Location supervisor scope | Source subscriptions, reload consumer, asynchronous update checks and initial hold |
| Location registry | Ordered activation slots, readiness tokens, inventory, activation lock and failure worker |
| Individual activation scope | Plugin registrations, listeners and resources acquired during setup |
| Triggering workflow | Invocation of a registered hook and its permitted failures |

[Plugin.load](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin.ts:46) forks an activation scope and supplies it to plugin setup. [PluginHooks.register](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin/hooks.ts:64) registers removal in the subscriber's scope and returns idempotent early disposal. `trigger` yields callbacks in the current workflow. Registration lifetime therefore does not dictate callback execution lifetime. The hook contract permits expected failures per operation; a common broad error union would weaken those permissions.

The small [Plugin service contract](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin/service.ts) is kept separate from its host implementation so session entrypoints can await activation without importing the host dependency cycle. A contract-only module is useful when dependency direction requires it.

## Readiness Tracks Accepted Work

Registry holds are tokens in a pending set controlling a `Latch`. Releasing one hold opens readiness only when every hold is released. Inventory can contain failed plugins once readiness settles. Requests needing plugin-provided state, such as [prompt preparation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/session/prompt.ts:41), await that contract before reading hooks or catalogs.

The supervisor's `observed` target tracks accepted notifications; its separate `generation` identifies activations and guards late update checks. These counters answer different questions. A latch opened after the first activation alone would admit requests while an already-accepted change is still pending.

## Keep Failure Paths Distinct

| Failure stage | Reviewed policy |
| --- | --- |
| Import/resolve a changed module | [Resolver](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin/supervisor.ts:66) reports failure and retains the last running generation because no replacement generation exists |
| Set up a new generation | [Registry activation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin.ts:122) closes the changed suffix before loading it; on setup failure it may load the previous healthy definition again as a fallback |
| Transform fails after setup | [Failure worker](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin.ts:178) records failure against the exact activation, refreshes inventory/state, and schedules scope cleanup; a failed activation is ineligible for fallback |
| Activation workflow fails | Supervisor reports the cause and checks whether the current notification target has settled; readiness does not promise every plugin succeeded |

Import retention preserves an existing running activation. Setup fallback is reactivation of an older definition after teardown, with different continuity guarantees. State those guarantees separately when designing replacement.

Failed-plugin finalizers can await readiness. The failure worker schedules their cleanup outside its activation lock/readiness hold, ensures cleanup is scheduled even when reporting fails, and releases its hold. Joining those finalizers while retaining the hold would create a wait cycle. [Registry close](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/src/plugin.ts:235) marks closure and opens readiness before joining shutdown. The supervisor also registers registry closure so plugins unload before the services its built-ins captured are finalized.

## Regression Evidence

These upstream tests were read, not executed.

| Contract | Test and observable assertion |
| --- | --- |
| Retain changes during boot | [Initial activation](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin/supervisor-reload.test.ts:196): gate setup, change a real source, await readiness, observe only the new command |
| Retain a healthy generation on import failure | [Broken local module](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin/supervisor-reload.test.ts:251): failure inventory coexists with the old command and active plugin |
| Serialize refresh with reload | [Periodic refresh](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin/supervisor-reload.test.ts:291): gate resolve, advance virtual time, observe peak concurrency of one |
| Remove only failed-plugin registrations | [Healthy-peer continuity](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin-failure.test.ts:13): hooks and RPC handlers from the healthy peer still work after failed-plugin cleanup |
| Avoid readiness/cleanup deadlock | [Reload and teardown](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin-failure.test.ts:71): a finalizer waits for readiness while replacement still completes |
| Keep a disabled fallback disabled | [Replacement setup failure](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin-failure.test.ts:141): the old failed definition is never loaded again |
| Open readiness before shutdown joins cleanup | [Gated shutdown](/Users/phtngyn/Developer/skills/repos/opencode/packages/core/test/plugin-failure.test.ts:261): shutdown completes despite a finalizer awaiting readiness; subsequent activation stays closed |

The selected tests do not independently isolate the late update-check generation guard or healthy setup fallback. Those claims come from implementation review; add controlled acceptance cases when they are part of a new application's public guarantees.

## Apply The Reasoning

A reloadable service can start with a scoped source subscription, one sequential consumer and explicit readiness. Add generation tracking when accepted work can overlap activation or late results can arrive after replacement. Choose whether a broken update retains the current resource, reconstructs a fallback, or disables the capability before implementing cleanup. Use [Concurrency](../../../skills/effect/references/CONCURRENCY.md) for competition policy and [Lifetimes](../../../skills/effect/references/LIFETIMES.md) for scope ownership.
