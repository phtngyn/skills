# Source and ownership

`SKILL.md` is a personal synthesis for preparing agent tasks. Its requirements come from the user's request on 2026-10-11: remain in a management role, start with rough ideas, clarify important intent with recommendations, and preview an execution prompt before passing it to an agent.

## Guidance considered

- [Matt Pocock's Grilling](https://github.com/mattpocock/skills/blob/f3fc5632f401156837ee3872f14fe33ccf1024ea/skills/productivity/grilling/SKILL.md): distinguish facts to discover from decisions to ask about, recommend answers, and respect question dependencies.
- [Matt Pocock's Handoff](https://github.com/mattpocock/skills/blob/f3fc5632f401156837ee3872f14fe33ccf1024ea/skills/productivity/handoff/SKILL.md): prepare context for another agent and reference existing artifacts instead of duplicating them.
- [Writing for Agents](https://github.com/mattpocock/skills/tree/f3fc5632f401156837ee3872f14fe33ccf1024ea/skills/productivity/writing-for-agents): keep context pointers precise, completion criteria clear, and instructions concise.
- [Official OpenAI prompting guidance](https://learn.chatgpt.com/docs/prompting), reviewed 2026-10-11: describe the desired result, useful context, boundaries, and verification in ordinary language.

## Personal choices

The skill uses a bounded interview and stops when the task can be delegated. It distinguishes accepted requirements, verified facts, proposals, assumptions, and unresolved decisions. Preparation alone grants no execution or transmission authority; authorization already present in the task is preserved.

These are personal adaptations, not unchanged upstream workflows or claims of endorsement. No upstream body is copied. The entry point has no runtime dependency on the upstream checkouts; they were authoring references at the adopted Matt revision recorded in [UPSTREAM.md](../../UPSTREAM.md). UI metadata uses Codex's bundled Skill Creator guidance and retains normal automatic discovery for requests to prepare an agent task.
