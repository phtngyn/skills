---
name: design
description: "Explicit design coordinator. Use $design or /design for UI craft, CSS, prototypes, motion, critique, and mobile web work."
---

# Design

Understand the experience, choose the right specialist, build within the product's conventions, and verify the result on its real surface. This family combines Emil Kowalski's UI craft with Vojta Holik's Good CSS techniques through local Codex adapters.

## Start and route

Start when the user invokes `$design` or `/design`. For a bare invocation, ask what to work on. Otherwise begin the requested task. Follow-ups continue it without another invocation.

Choose the most specific subskill below and read it once; combine specialists only when needed. Each can also be invoked directly and selects its references by task. Reuse bodies already supplied in messages and material already loaded in this context. A specialist owns its task method and output.

| Request | Subskill |
| --- | --- |
| General UI craft, implementation, or critique | [design-ui](../design-ui/SKILL.md) |
| CSS layout, sizing, typography, overflow, or native controls | [design-css](../design-css/SKILL.md) |
| Explore competing visual or interaction directions | [design-prototype](../design-prototype/SKILL.md) |
| Build or fix web motion | [design-animate](../design-animate/SKILL.md) |
| Diagnose dropped frames or choose animation properties and drivers | [design-animation-performance](../design-animation-performance/SKILL.md) |
| Review existing motion or a motion diff | [design-review-animations](../design-review-animations/SKILL.md) |
| Audit motion and plan improvements | [design-improve-animations](../design-improve-animations/SKILL.md) |
| Find worthwhile places to add motion | [design-find-animation-opportunities](../design-find-animation-opportunities/SKILL.md) |
| Remove unnecessary or excessive motion | [design-remove-animations](../design-remove-animations/SKILL.md) |
| Name an animation effect | [design-animation-vocabulary](../design-animation-vocabulary/SKILL.md) |
| Apple-inspired physical interaction or visual design | [design-apple](../design-apple/SKILL.md) |
| Mobile web polish and touch behavior | [design-mobile](../design-mobile/SKILL.md) |
| Stress UI with difficult data | [design-break-ui](../design-break-ui/SKILL.md) |

A request to explore alternatives selects `design-prototype`; a narrow fix or agreed implementation does not. If an audit or critique becomes an implementation request, continue with the matching construction specialist rather than requiring another command.

## CSS implementation support

Read [design-css](../design-css/SKILL.md) when implementing or reviewing styles alongside the selected specialist. Reuse guidance already loaded. Prefer Tailwind when practical for a new project, preserve an established styling system or explicit user choice, and use custom CSS where utilities obscure intent or cannot express the behavior.

Read [CSS integration](references/CSS_INTEGRATION.md) when CSS mechanisms overlap with motion or mobile behavior. It resolves the specific source conflicts without replacing either source's detailed guidance.

## Sources

The selected specialist applies the shared [source rules](references/SOURCES.md). The [implementation workflow](references/WORKFLOW.md), [delegation notes](references/DELEGATION.md), and [source map](references/SOURCE_MAP.md) are conditional references, not startup requirements. Do not route to `ask-sonner`, `pick-ui-library`, `write-swift`, or `animate-expo`, including through upstream references. The upstream checkouts remain unchanged, outside the installed family.

See [source and ownership](PROVENANCE.md) for the adopted sources and maintenance boundaries.
