---
name: audit
description: Keep an evidence-backed decision trail and obtain a separate review for substantial, long-running, unattended, or consequential work. Use when several meaningful decisions need review; skip routine edits, short explanations, and simple fixes.
---

# Audit

Use this support workflow when a task needs a reviewable decision trail or the user requests it. Continue the active task's guidance.

## Select and load

For automatic selection, choose it for several consequential decisions, unattended work, or verification that needs a durable record. Task size alone is insufficient; handle routine edits, short explanations, and simple fixes directly.

Read Poteto's original [Show Me Your Work](../../repos/pstack/pstack/skills/show-me-your-work/SKILL.md) and follow its logging format, helper, append-only corrections, run boundaries, and evidence rules. Resolve references from its directory and reuse any trail already active for this task. These local rules take precedence over conflicting upstream instructions.

Tell the user briefly when activating the workflow. Record decisions from activation onward; identify any earlier evidence as retrospective rather than inventing a contemporaneous history. Keep the log as a local working artifact unless committing it is authorized.

## Audit available evidence

Use the current task's transcript when available. Otherwise review its messages, source changes, commands, test output, and recorded artifacts. Disclose the unavailable transcript comparison and identify the evidence reviewed; an artifact review does not establish a complete transcript audit. Access only this task's evidence.

## Separate review

Before the final handoff, use one separate subagent to review the completed trail and its supporting work when delegation is available and permitted. This workflow requests that focused review; it does not authorize unrelated delegation or external actions.

Give the reviewer accepted requirements, the trail, changed files or diff, tests and raw results, artifact locations, and any task transcript. Let it reach independent conclusions without the builder's verdict or suspected findings. It checks the work and supporting evidence, without rebuilding the task or starting another trail or reviewer chain.

Use a separate agent with the inherited model; a different model family is unnecessary. Report model identity only as exposed by the host, distinguishing a requested model from a verified backend identity. If delegation is unavailable, report that separate review was not performed; self-review does not satisfy it.

Inspect the findings and evidence, correct supported issues within scope, and append the resulting decisions. Request focused reassessment from the same reviewer when a correction materially changes the reviewed work.

## Handoff

In the final response, link the canonical trail and end with the upstream Attention section: identify the reviewer as accurately as the host permits, point to concrete concerns, and disclose missing transcript or review evidence. Use “No flags” only when the review occurred and found none. Progress updates can remain concise without repeating this section.

The original source and bundled resources remain unchanged. See [provenance](PROVENANCE.md) and the collection's [upstream pins](../../UPSTREAM.md). If the source is missing or differs from its adopted pin, report that condition instead of silently substituting it.
