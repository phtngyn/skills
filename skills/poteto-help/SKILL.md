---
name: poteto-help
description: Guides users through pstack setup, $poteto-mode, and picking the skill, playbook, or principle for a task. Type $poteto-help with a question.
---

# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [poteto-mode](../poteto-mode/SKILL.md) and do the work under it.

This file maps questions to the installed skills and playbooks that hold the answers. Read the file you route to before quoting it.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `$poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- If `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json` is missing, workers inherit the active Codex settings.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `$create-verification-skill` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `$create-formal-verification-skill` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `$maintain-formal-verification-skill` if the question touches that code.

When role preferences are absent and model choice matters, explain inheritance and offer [$setup-pstack](../setup-pstack/SKILL.md) once:

- Now: give them `$setup-pstack` to type, and answer their question too.
- Later: answer their question and explain that roles inherit the active model until configured.

## Get set up

1. Install the collection using [setup](../../README.md#install). Start a new chat after installing new skills so Codex can discover them.
2. Run [$setup-pstack](../setup-pstack/SKILL.md) if the user wants optional model or effort preferences.
3. Start a real task with `$poteto-mode`, a goal, and a check that can pass or fail.

For app verification, see [$create-verification-skill](../create-verification-skill/SKILL.md) and [$create-formal-verification-skill](../create-formal-verification-skill/SKILL.md). Word a first prompt with [prompting.md](references/prompting.md) when asked.

If cost is the worry, explain that parallel workers and review panels add work. Use a shorter panel or a supported model or effort preference when the user wants to reduce that work. Ordinary tasks can stay in the active Codex thread.

## Start a task with `$poteto-mode`

`$poteto-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one.

Use `$poteto-mode` at the start of a new task. Mid-chat, "new task" signals that Codex should match a fresh playbook. See the [runtime guidance](../poteto-mode/references/codex.md) for authorized delegation and worker briefs.

## Pick a skill

The default answer is `$poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`$poteto-mode`](../poteto-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`$in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`$sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`$how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`$why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`$teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`$recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`$ketchup`](../ketchup/SKILL.md) |
| Catch up like `$ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`$ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`$blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`$architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`$arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as Codex workers | [`$swarm`](../swarm/SKILL.md) |
| Have independent Codex reviewers examine a diff and try to break it | [`$interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`$tdd`](../tdd/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`$no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`$unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`$technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`$bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`$create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`$maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`$create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`$maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`$statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`$benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`$figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`$show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`$setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`$automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`$reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`$correct`](../correct/SKILL.md) |
| Find their way around pstack | `$poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `$how` explains what the code does. `$why` explains the reasons. `$teach` runs one or both and explains the result plainly.
- `$arena` gives every worker the same brief and merges the best parts. `$swarm` splits work into slices or a race and returns one report.
- `$interrogate` reviews the diff. `$blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `$recall` rebuilds context across recent chats. `$ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `$figure-it-out` designs one rigorous run. The Autonomous run playbook drives one task to a finish condition.

## Playbooks and principles

Playbooks are step lists inside `$poteto-mode`. Within it, describe the task or use one of these phrases:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

The [Playbooks section](../poteto-mode/SKILL.md#playbooks) lists all bundled playbooks.

Codex Plan mode works alongside Poteto. For work that spans phases or stacked PRs, asking `$poteto-mode` for a plan runs the [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and stops at handoff. For a design question, use [Prototype](../poteto-mode/playbooks/prototype.md) or `$architect`.

Principles are one-rule skills that `$poteto-mode` reads and cites when they apply. Steer by the names, as in "apply prove it works. show me the real output." Invoke a leaf directly with `$principle-<name>`. [Poteto mode](../poteto-mode/SKILL.md#principles) lists the principles.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying | Start the next task with `$poteto-mode`. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | Confirm the setting is supported by the active host and configured for the relevant role. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Invoke it with `$skill-name`. Poteto reads bundled skills when a step needs them. |
| Parallel agents overwrote each other | Give concurrent writers separate host-managed checkouts. |
| An overnight run moved but finished nothing | Use a checkable finish condition. See [Autonomous run](../poteto-mode/playbooks/autonomous-run.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [prompting.md](references/prompting.md) has one-line steers and [recipes.md](references/recipes.md) offers complete examples.

## Make pstack my own

- [`$automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `$poteto-mode`.
- [`$reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `$poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
