---
name: design-css
description: "Implement or review CSS layout, sizing, typography, overflow, native controls, and responsive behavior within the project's styling system."
---

# CSS

Read the [source rules](../design/references/SOURCES.md) once, reusing them if already loaded. Read [Good CSS integration](../design/references/GOOD_CSS.md), then the upstream entries it selects. Resolve upstream reference categories from the Good CSS checkout.

## Task and Codex adaptations

Use supported native CSS and intrinsic layout where they preserve the required behavior. Keep the project's tokens, palette, resets, breakpoints, and established styling system. Good CSS's CSS-first preference concerns presentation; application state, data loading, and necessary focus management can still require JavaScript.

Prefer Tailwind when practical for new projects without an established styling system. Translate techniques into supported utilities, variants, or arbitrary properties when clear, preserving logical properties. Use small custom rules where utilities obscure intent or cannot express the mechanism. Check the installed Tailwind version before relying on newer utilities.

Use [CSS integration](../design/references/CSS_INTEGRATION.md) for overlapping motion or mobile advice. Motion purpose and behavior come from the matching Design motion specialist, not a CSS recipe. Check project browser targets and required semantics as well as appearance. Report unavailable browser verification rather than treating a support note as runtime proof.
