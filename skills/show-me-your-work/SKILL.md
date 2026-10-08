---
name: show-me-your-work
description: Keep an evidence-backed decision trail and obtain a separate review for substantial, long-running, unattended, or consequential work. Use when several meaningful decisions need review; skip routine edits, short explanations, and simple fixes.
---

# Show Me Your Work

Use this shared support workflow when the task warrants a reviewable decision trail, or when the user explicitly requests it. Continue the active task's specific guidance.

## Select and load

For automatic selection, consider whether the work spans several consequential decisions, proceeds unattended, or needs a durable record to assess its verification. Task size alone does not require a trail. Handle routine edits, short explanations, and simple fixes directly.

When selected, read Poteto's original [Show Me Your Work](../../repos/pstack/pstack/skills/show-me-your-work/SKILL.md). Follow its logging format, helper, append-only corrections, run boundaries, and evidence rules. Resolve its references from the upstream directory. Reuse a trail already active for this task instead of starting a second one. These local integration rules take precedence over conflicting upstream instructions.

Tell the user briefly when activating the workflow. Record decisions from activation onward; identify any earlier evidence as retrospective rather than inventing a contemporaneous history. Keep the log as a local working artifact unless committing it is authorized.

## Audit available evidence

Use the current task's transcript when the host exposes it. Otherwise inspect the available task messages, source changes, commands, test output, and other recorded artifacts. Report the transcript comparison as unavailable and describe the actual evidence reviewed; an artifact review does not establish a complete transcript audit. Access only evidence belonging to the current task.

## Separate review

Before the final handoff, use one separate subagent to review the completed trail and its supporting work when delegation is available and permitted. This workflow requests that focused review; it does not authorize unrelated delegation or external actions.

Give the reviewer the accepted requirements, trail, changed files or diff, relevant tests and raw results, artifact locations, and available task transcript. Let it reach its own conclusions rather than supplying the builder's verdict or suspected findings. The reviewer checks what happened and whether the evidence supports the claims; it does not rebuild the task or begin another trail or reviewer chain.

Prefer a different model family when the host exposes one and model selection is authorized. Otherwise use a separate agent with the inherited model, and label it as separate-agent review with cross-family independence unmet. Report model identity only to the extent the host exposes it; distinguish a requested model from a verified backend identity. If delegation is unavailable, report that independent review was not performed; self-review does not satisfy it.

Inspect the reviewer's findings and evidence yourself. Correct supported issues within the task's scope and append the resulting decisions. If a correction materially changes the reviewed work, request a focused reassessment from the same reviewer; do not repeat the full task merely to review it.

## Handoff

In the final response, link the canonical trail and end with the upstream Attention section: identify the reviewer as accurately as the host permits, point to concrete concerns, and disclose missing transcript or cross-family verification. Use “No flags” only when the review occurred and found none. Progress updates can remain concise without repeating this section.

The original source and bundled resources remain unchanged. See [provenance](PROVENANCE.md) and the collection's [upstream pins](../../UPSTREAM.md). If the source is missing or differs from its adopted pin, report that condition instead of silently substituting it.
