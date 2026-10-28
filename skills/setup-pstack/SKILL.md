---
name: setup-pstack
description: Configure pstack models per role and reasoning budget. Use for $setup-pstack or changing pstack's model choices.
---

# Setup pstack

Write `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json` with optional model choices per role. Unconfigured roles inherit the parent model. This file is read by the skills, not applied globally.

## Steps

1. Detect the model and reasoning-effort choices supported by the active agent tools. Do not write an unverified model name. `inherit-parent` and `auto` keep the parent model.
2. Load the existing JSON if present. Preserve the current budget and role choices; drop retired roles.
3. Ask for a budget: `unlimited` requests max, `large` requests xhigh, `medium` requests high, and `small` requests medium. Apply supported efforts to real model entries, keeping inheritance unchanged. Show the resulting roles and ask which choices to change. Do not replace a configured model family with another without a user choice.
4. Validate every chosen model and reasoning effort against the available set.
5. Write `budget` and `roles` as JSON. A role value is an object with `model` and optional `reasoning_effort`. Panel and pool values are lists of these objects; panel length sets the agent count and a pool supplies one cross-judge. Preserve unspecified choices and parse the written file to validate it.
6. Report the path and effective choices. They apply when a skill next reads them.
7. If the project has no way to drive the app for proof, offer once to create one with `$create-verification-skill`.

Roles: `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `hardest tasks`, `how explorer`, `how explainer`, `why investigators`, `why synthesizer`, `reflect tooling`, `reflect judgment, divergent, synthesizer`, `swarm workers`.

Panels: `arena runners`, `architect runners`, `interrogate reviewers`. Pool: `arena cross-judge pool`.
