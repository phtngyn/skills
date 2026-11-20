---
name: setup-pstack
description: Configure optional Codex model and effort preferences for Poteto delegation roles. Use for $setup-pstack or when changing Poteto's model choices.
---

# Setup pstack

Use `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json`. Poteto reads it at invocation time. Roles inherit the active Codex model and effort when the file or role is absent. This is skill configuration. The host still controls which model overrides are available.

1. Read the existing file and the active tool's model and effort options. Use only confirmed Codex model IDs and supported effort for the current host. Keep inheritance available even when overrides are unsupported.
2. Read the saved budget before proposing changes. If the user asks for a budget, offer `large` (xhigh), `medium` (high), or `small` (medium), limited to what the selected Codex models support. Apply the chosen effort to confirmed single-role model entries. Keep inherited roles and deliberate panel settings intact. Preserve the previous budget on a targeted role edit.
3. Apply the role changes the user requests. Preserve other valid entries. If the request lacks a necessary choice, use the host question tool or ask in chat. Tell the user when a requested setting is unsupported. Leave the prior choice in place unless the user asks to clear it.
4. Write valid JSON and read it back. Report the path, changed roles, and which settings inherit. This does not start an agent or alter global settings.

Entries are objects with `model` and optional `reasoning_effort`. Omit an entry to inherit, or use `"model": "inherit-parent"` with no effort. Panel entries are arrays of the same objects. Record the chosen `budget` label alongside `roles` when budget was requested. An empty file configuration is `{"roles": {}}`.

Single roles: `feature, refactoring` (one shared key), `bug-fix`, `perf-issue`, `hillclimb`, and `swarm workers`.

Panel roles: `arena runners` and `interrogate reviewers`. Their lengths set the requested panel size within available capacity. For `arena cross-judge pool`, choose the first supported entry and run one judge. Leave unrelated existing keys intact.

Read the [Codex runtime guidance](../poteto-mode/references/codex.md) before applying these preferences.
