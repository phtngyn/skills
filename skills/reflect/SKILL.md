---
name: reflect
description: "Review the current conversation for recurring lessons and propose or apply authorized improvements to existing skills."
---

# Reflect

Review the active conversation for durable lessons and route them to existing skills.

## Gather evidence

Use the visible conversation or an explicitly identified transcript for this session. If no transcript is exposed, prepare a concise digest with the user's corrections, decisions, failures, and artifacts. State its limits. Do not search unrelated session stores.

## Review

Read the [Codex delegation contract](../poteto-mode/references/codex.md). Launch three read-only reviewers using `references/judgment-reviewer.md`, `references/tooling-reviewer.md`, and `references/divergent-reviewer.md`. Use role `reflect tooling` for tooling, and `reflect judgment, divergent, synthesizer` for the others. Give them the transcript path or digest, and only the tool access necessary to check its cited evidence.

Use a fresh synthesizer with `references/synthesizer.md` to produce Accepted, Rejected, and Backlog lists. If delegation is unavailable, perform the lenses sequentially and disclose that limitation.

## Apply

Move findings best enforced by types, lint, scripts, or runtime checks to Backlog, following `principle-encode-lessons-in-structure`. Prefer existing skills and repeated evidence. A one-off is not a universal rule.

Present the proposed edits for approval unless the user already authorized applying reflection findings. Apply only the authorized subset. Use Codex's `skill-creator` for substantive skill changes and validate touched skills. Keep backlog items local unless filing them externally was explicitly authorized.

Never edit a skill under `plugins/cache/`. Resolve installed symlinks to their maintained source. For a cache-owned skill without a writable source, show the proposed destination under `~/.agents/skills/` or the project’s skill directory before approval, then copy and edit it there. Reflection alone does not authorize a push or PR.

Report applied edits, unresolved proposals, and rejected findings with reasons.
