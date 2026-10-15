---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for $swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

Run bounded workers over separate slices, identical briefs, or a mixture, then return one report.

## Frame

State the done predicate and artifact. Choose partitioned coverage, a race, or best-of comparison before launching. Set the total worker count from the request or the useful decomposition, independently of the concurrency limit.

Read the [Codex delegation contract](../poteto-mode/references/codex.md), role `swarm workers`. Inherit the current model by default. Use isolated worktrees or output directories for writers. Every measurement brief names exact revisions, method, sample count, and ordering.

## Fan out

Launch workers with the available Codex agent tool, up to its concurrency limit. Each brief stands alone: goal, scope, owned paths, input revision, verification, stopping condition, and report shape. Workers report `PASS`, `ISSUES`, or `BLOCKED`, with evidence. A proven defect is `ISSUES`, even when other checks passed.

For `first pass`, accept the first qualifying proof and stop remaining work cleanly. For `rank all`, collect every result. For `best-of`, collect enough complete results for the declared comparison. Do not silently switch modes.

If delegation is unavailable, cover slices sequentially and report that a parallel swarm did not run. Never describe direct work as independent verification.

## Aggregate

Inspect artifacts, not just reports. Reconcile overlapping findings, reproduce consequential claims, and preserve disagreements and missing coverage. A dropout is missing coverage, not a pass. Stop or interrupt surplus workers, and retain their useful artifacts.

## Report

Return the overall verdict, per-slice outcomes, evidence paths, proven issues, and blocked or omitted coverage. Keep raw worker output outside the main response.
