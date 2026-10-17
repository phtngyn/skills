# Application Examples

OpenCode v2 and T3 Code show how Effect supports two substantial applications. Use them to understand a decision's requirements, ownership, failure policy and observable guarantees. Effect's declarations and tests establish API behavior; the consuming project's requirements determine which application patterns fit.

## Choose The Relevant Workflow

| Decision | OpenCode v2 | T3 Code |
| --- | --- | --- |
| Construct and share capabilities | [Graph composition and adapter replacement](OPENCODE.md#composition-and-replacement) | [Shared Layers and transport-independent capabilities](T3_CODE.md#keep-capabilities-reachable-across-transports) |
| Coordinate concurrent work | [Join, coalesce and stop session execution](OPENCODE_SESSION.md#choose-the-competition-and-stop-contracts) | [Accept commands and execute durable work](T3_CODE.md#separate-durable-acceptance-from-execution) |
| Own resources and replacement | [Keyed service graphs](OPENCODE.md#keyed-service-graphs), [subscriber replacement](OPENCODE_PLUGINS.md#separate-the-owners) | [Process-local signals and durable state](T3_CODE.md#keep-capabilities-reachable-across-transports) |
| Define completion | [Refresh readiness](OPENCODE_PLUGINS.md#readiness-tracks-accepted-work), [cancellation and settlement](OPENCODE_HOST.md#cancellation-and-settlement) | [Committed acceptance, execution and recovery](T3_CODE.md#separate-durable-acceptance-from-execution) |
| Deliver events | [Host-owned streams and iterators](OPENCODE_HOST.md#plugin-context-iterators-and-representation) | [Publication order](T3_CODE.md#preserve-publication-order-explicitly), [bounded replay and live delivery](T3_CODE.md#bound-the-whole-replay-and-live-pipeline) |
| Verify a race or lifecycle | [Session](OPENCODE_SESSION.md#regression-evidence), [reload](OPENCODE_PLUGINS.md#regression-evidence), [host](OPENCODE_HOST.md#regression-evidence) | [Admission, settlement, publication and stream regressions](T3_CODE.md#regression-evidence-and-executed-checks) |

Read the workflow that matches the current problem. Neither application needs to be loaded in full for an ordinary edit.

## Apply The Contract

Start with what the caller needs. Decide whether concurrent calls join, queue, replace or coalesce; whether completion means admission, execution or cleanup; and whether events need live notification, a current snapshot or durable replay. Choose the resource and execution owner separately from any persisted intent.

Then trace the example's construction, execution, failure and cleanup paths. Identify which mechanism enforces the guarantee and which test observes it. Translate that relationship into the consuming domain. A keyed mutex does not provide durable delivery, a durable queue does not define caller cancellation, and stored history does not bound the memory used to deliver it.

Use the smallest design that satisfies the contract. Ordinary Layers can express shared capability graphs; a custom graph compiler earns its complexity only when replacement and sharing requirements need it. Finite programs and reusable libraries often retain caller-owned execution without application services or persistence.

The topic guides own general guidance. These examples supply source evidence and tradeoffs. Package layout, import style, graph helpers, retention periods and test runners remain application conventions. Reviewed revisions and executed-check limits are recorded in [provenance](../PROVENANCE.md).
