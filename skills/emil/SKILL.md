---
name: emil
description: "Explicit design entry point. Use /emil to route UI design, prototyping, animation, review, and mobile work to Emil Kowalski's upstream skills."
---

# Emil

Use Emil Kowalski's upstream skills directly. This file coordinates them; it does not replace their guidance or impersonate their author.

## Entry and routing

For `/emil <request>` or `$emil`, inspect the request and relevant project context, then read the matching upstream `SKILL.md` below. Follow its workflow and load its referenced resources when needed. The exclusions and personal preferences in this wrapper take precedence over conflicting upstream instructions. Resolve upstream links relative to that upstream skill's directory. Do not substitute remembered summaries for reading the selected material.

For a bare invocation, ask what the user wants to work on. Otherwise proceed with the actual request without a readiness greeting. The user does not need to invoke a second command.

| Request | Upstream skill |
| --- | --- |
| General UI craft, implementation, or design critique | [emil-design-eng](../../repos/emil/skills/emil-design-eng/SKILL.md) |
| Explore multiple UI directions | [prototype](../../repos/emil/skills/prototype/SKILL.md) |
| Build or fix web motion | [animate](../../repos/emil/skills/animate/SKILL.md) |
| Review existing motion or a motion diff | [review-animations](../../repos/emil/skills/review-animations/SKILL.md) |
| Audit existing motion and plan improvements | [improve-animations](../../repos/emil/skills/improve-animations/SKILL.md) |
| Find worthwhile places to add motion | [find-animation-opportunities](../../repos/emil/skills/find-animation-opportunities/SKILL.md) |
| Name an animation effect | [animation-vocabulary](../../repos/emil/skills/animation-vocabulary/SKILL.md) |
| Apple-inspired physical interaction or visual design | [apple-design](../../repos/emil/skills/apple-design/SKILL.md) |
| Mobile web polish and touch behavior | [mobile-native](../../repos/emil/skills/mobile-native/SKILL.md) |
| Stress UI with difficult data | [break-ui](../../repos/emil/skills/break-ui/SKILL.md) |

Choose the most specific skill for the task. Combine relevant skills for a mixed request; avoid loading the entire collection. An explicit request to explore alternatives through `/emil` counts as requesting the prototype capability, even though its upstream skill requires explicit invocation. Do not introduce that workflow merely because it is available.

Excluded from this mode: `ask-sonner`, `pick-ui-library`, `write-swift`, and `animate-expo`. Do not route to or load these skills, including when another upstream skill references them. Handle incidental library decisions using the project’s existing conventions and ordinary research; keep this mode focused on web design and motion.

## CSS implementation support

For CSS implementation or review, read our [Good CSS entry point](../good-css/SKILL.md) alongside the selected Emil workflow. It loads matching upstream techniques and defines integration priorities. Reuse guidance already read and continue the current workflow.

## Personal preferences and Codex integration

These are the wrapper's adjustments to upstream behavior:

- Discover project facts yourself. Discuss consequential ambiguous requirements or design direction with the user, with a recommendation. Once direction is settled, implement autonomously within the requested scope.
- Preserve the full requested scope. For multi-component exploration, agree on staging rather than silently reducing the request to one component.
- Respect the project's design system, components, dependencies, and established product decisions. Retain upstream craft guidance and detailed techniques; do not rewrite them into generic advice.
- Use tools available in Codex for the same intended outcome. If an upstream workflow assumes another agent environment, adapt the tool mechanics. Delegate only when authorized. Do not commit, publish, create PRs, or message others without task authorization.
- Honor whether the request is for critique, planning, exploration, or implementation. An audit may produce plans; when the user asks to implement selected changes, continue with the appropriate construction skill rather than requiring a separate command.
- Verify version-sensitive API and performance claims against the installed implementation or current official documentation when relevant. If upstream instructions conflict internally, use their specific component guidance and explain consequential tradeoffs rather than silently applying contradictory rules.
- Follow-up messages continue the current design task without requiring `/emil` again. This is not an application-wide persistent mode.

## Source availability and updates

Source links point outside the installed wrapper to the local Emil checkout’s `skills/` directory. Read it as the source of design guidance. If the checkout is unavailable, report the missing checkout rather than silently using another installed skill with the same name.

Resolve the real path of this wrapper before resolving relative source links. Do not nest upstream directory links under the installed wrapper; they expose excluded skills as independent entries.

The checkout must remain at the Emil based-on commit recorded in the collection's `UPSTREAM.md`. Fetching updates remote refs; it does not authorize advancing the checkout. During an update review, compare new upstream changes and recommend adoption. Advance the checkout and recorded based-on commit together only when the update is adopted.

See [provenance](PROVENANCE.md) for ownership and layout.
