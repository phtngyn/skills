---
name: automate-me
description: "Create or update a personal mode skill from the user\u2019s stated preferences and recurring working habits."
---

# Automate me

Turn the user's working conventions into one personal `<handle>-mode` skill.

1. Inspect project `.agents/skills/` and the configured personal skill directory for an existing matching mode. Resolve symlinks before editing. Update an existing mode in place unless the user asks to replace it.
2. Gather recurring preferences from the current conversation and explicitly provided workspace-scoped history. Read the [Codex history and delegation contract](../poteto-mode/references/codex.md). When history is unavailable, use the visible conversation and ask one or two focused questions about missing preferences. Never scan unrelated chats.
3. For substantial history, split it into bounded slices and have read-only agents return patterns with evidence. Require repeated evidence before generalizing. An explicit user preference is authoritative without repeated examples.
4. Group findings only where the user has non-default rules: response style, autonomy, code, verification, delegation, or delivery. Read `poteto-mode` for granularity, not content to copy.
5. Use Codex's `skill-creator`. Preserve an existing destination; otherwise use `.agents/skills/<handle>-mode/` for a project mode or the configured personal skill directory for a personal mode. Use a description specific to this user's style. Let skill-creator establish supported invocation metadata, preserving an existing policy.
6. Apply `unslop`, show the actual draft, and incorporate feedback. Validate the skill and all references. Commit or open a PR only when the task's delivery scope includes it.

Keep the mode short. Link to other skills rather than copying their contents. Preserve earlier preferences unless the user contradicts them. Do not infer blanket external-action permission from a preference for autonomy.
