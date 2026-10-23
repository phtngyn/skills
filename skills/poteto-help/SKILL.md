---
name: poteto-help
description: "Explain this Codex skill collection, recommend a workflow, and help write a concrete task prompt without starting the task."
---

# Poteto help

Answer questions about this Codex collection and recommend a matching workflow. A help question does not authorize executing the suggested task. Read the recommended skill or playbook before explaining it, and link to its local source.

## Setup

The collection README documents `scripts/setup.sh`, which links skills into `~/.agents/skills`. Start a new chat after installation to refresh discovery. Invoke a skill with `$skill-name`.

Poteto skills preserve upstream explicit-only invocation through `agents/openai.yaml`. A workflow can read sibling skill instructions by path when its phases require them. `$poteto-mode` is the general execution entry point; it does not install a persistent mode. `$setup-pstack` optionally records role preferences; otherwise all agents inherit the current model.

Read [the Codex contract](../poteto-mode/references/codex.md) for delegation, history, model availability, and live-control fallbacks. This collection includes neither Benny nor the bot UI skill.

## Choose a workflow

- Goal understanding: `in-your-own-words`. Rewrite a task prompt without executing it: [sharpen](../sharpen/SKILL.md).
- Current architecture and flow: `how`. Historical rationale: `why`. A combined explanation: `teach`.
- Recent project context: `recall`. Progress and every pending decision within this chat: `ketchup`. A simpler last reply: `bro`.
- General execution: `poteto-mode`. Ambitious unfamiliar work: `figure-it-out`.
- Interface and module design: `architect`. Competing solutions: `arena`. Parallel coverage: `swarm`.
- Adversarial review: `interrogate`. Downstream breakage: `blast-radius`. Comment review: `no-comments`.
- Bug regression tests: `tdd`. Performance measurement: `benchmark-checklist`.
- Model-backed charts of user-visible behavior: `statechart`.
- App-driving harness: `create-verification-skill`. Harness and map upkeep: `maintain-verification-skill`.
- Writing: `technical-writing` and `unslop`.
- Personal conventions: `automate-me`. Session lessons: `reflect`. Structural prevention of repeated mistakes: `correct`.
- Auditable execution: `show-me-your-work`. Agent role preferences: `setup-pstack`.
- UI craft: `design`. Effect v4: `effect`.

The 24 `principle-*` skills guide decisions; `poteto-mode` indexes their triggers. Read a leaf before applying it.

## Playbooks

Read the Playbooks section in [poteto-mode](../poteto-mode/SKILL.md) for all 23 routes. A status check uses Babysit's single-pass mode; a request to get a PR green uses its bounded driving mode. Shipping needs a shipping request. Planning a multi-phase change produces a plan rather than implementing it.

## Prompt guidance

For help wording a task, read [prompting](references/prompting.md) and matching [recipes](references/recipes.md). Give one copyable prompt naming the outcome and a checkable completion condition. Explain missing capabilities precisely instead of promising model diversity, history access, or monitoring the host does not provide.
