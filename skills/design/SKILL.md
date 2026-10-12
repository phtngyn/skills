---
name: design
description: "Explicit design entry point. Use /design for UI design, CSS, prototyping, animation, review, and mobile work with Emil Kowalski's skills and Good CSS."
---

# Design

Use Emil Kowalski's upstream skills and Vojta Holik's Good CSS techniques through the workflows below.

## Entry and routing

For `/design <request>` or `$design`, inspect the request and relevant project context. Read the matching guidance in full, follow its workflow, and load references when needed. Resolve resources from the upstream skill's directory. This wrapper's exclusions and personal preferences take precedence over conflicting upstream instructions.

For a bare invocation, ask what to work on. Otherwise begin the requested critique, plan, exploration, or implementation. Follow-ups continue the current task without another invocation.

| Request | Guidance |
| --- | --- |
| CSS layout, sizing, typography, overflow, or native controls | [Good CSS](references/GOOD_CSS.md) |
| General UI craft, implementation, or design critique | [emil-design-eng](../../repos/emil/skills/emil-design-eng/SKILL.md) |
| Explore multiple UI directions | [prototype](../../repos/emil/skills/prototype/SKILL.md) |
| Build or fix web motion | [animate](../../repos/emil/skills/animate/SKILL.md) |
| Diagnose dropped frames or choose animation properties and drivers for performance | [animation-performance](../../repos/emil/skills/animation-performance/SKILL.md) |
| Review existing motion or a motion diff | [review-animations](../../repos/emil/skills/review-animations/SKILL.md) |
| Audit existing motion and plan improvements | [improve-animations](../../repos/emil/skills/improve-animations/SKILL.md) |
| Find worthwhile places to add motion | [find-animation-opportunities](../../repos/emil/skills/find-animation-opportunities/SKILL.md) |
| Name an animation effect | [animation-vocabulary](../../repos/emil/skills/animation-vocabulary/SKILL.md) |
| Apple-inspired physical interaction or visual design | [apple-design](../../repos/emil/skills/apple-design/SKILL.md) |
| Mobile web polish and touch behavior | [mobile-native](../../repos/emil/skills/mobile-native/SKILL.md) |
| Stress UI with difficult data | [break-ui](../../repos/emil/skills/break-ui/SKILL.md) |

Choose the most specific skill, combining relevant guidance for mixed requests. An explicit request to explore alternatives through `/design` satisfies prototype's invocation requirement; use that workflow only when exploration is requested.

Excluded from this mode: `ask-sonner`, `pick-ui-library`, `write-swift`, and `animate-expo`. Do not route to or load these skills, including when another upstream skill references them. Handle incidental library decisions using the project’s existing conventions and ordinary research; keep this mode focused on web design and motion.

## CSS implementation support

For CSS implementation or review, read our [Good CSS reference](references/GOOD_CSS.md) alongside the selected Emil workflow. It loads matching techniques and defines integration priorities. Reuse guidance already read.

Prefer Tailwind CSS when it fits the project's framework and constraints. Reuse an existing setup; choose Tailwind for new projects or those without an established styling system when practical. Honor explicit user choices and established styling conventions. Use custom CSS when utilities obscure intent or cannot express the required behavior.

## Personal preferences and Codex integration

- Discover project facts yourself. Bring consequential uncertainty about requirements or design direction to the user with a recommendation. Once settled, implement autonomously within scope.
- Preserve the full requested scope. For multi-component exploration, agree on staging rather than silently reducing the request to one component.
- Respect the project's design system, components, dependencies, and established product decisions. Retain upstream craft guidance and detailed techniques; do not rewrite them into generic advice.
- Adapt upstream tool mechanics to Codex while preserving the intended outcome. Delegate, commit, publish, create PRs, or message others only within task authorization.
- Honor whether the request is for critique, planning, exploration, or implementation. When the user asks to implement changes from a critique or plan, continue with the matching implementation workflow without requiring another command.
- Verify version-sensitive API and performance claims against the installed implementation or current official documentation when relevant. If upstream instructions conflict internally, use their specific component guidance and explain consequential tradeoffs rather than silently applying contradictory rules.

## Source availability and updates

Resolve this wrapper's real path before following relative links to the local Emil and Good CSS checkouts. Keep upstream directory links outside the installed wrapper so excluded skills stay undiscoverable through it.

Each selected checkout must match its based-on commit in [UPSTREAM.md](../../UPSTREAM.md). Report missing or mismatched sources instead of substituting another installed skill. Fetching preserves the checkout; review updates and advance the clean checkout and based-on record together when adoption is agreed.

See [provenance](PROVENANCE.md) for ownership and layout.
