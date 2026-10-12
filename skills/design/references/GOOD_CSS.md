# Good CSS

Use Vojta Holik's upstream CSS techniques directly. This internal Design reference coordinates their use with the project's conventions and our Design workflow; it does not replace the original guidance.

## Load the matching techniques

Read the upstream [Good CSS entry point](../../../repos/good-css/skills/good-css/SKILL.md), then use its routing table to locate matching reference categories. Resolve those references from that upstream directory. Search category headings and read matching entries in full, including their conditions and support notes. Keep each read bounded so the complete entry arrives without truncated aggregate output. Reuse entries already read and keep unrelated techniques unloaded.

Prefer intrinsic layout and supported native CSS mechanisms where they preserve the required behavior. Use the project's styling system and established tokens. Apply changes within the requested scope; introducing this skill does not require replacing an existing reset, palette, breakpoint system, or component library. Its CSS-first preference governs presentation techniques; application state, data loading, and necessary focus management can still require JavaScript.

Apply the [Design wrapper's Tailwind preference](../SKILL.md#css-implementation-support) to these techniques. Translate upstream CSS examples into Tailwind utilities, variants, or arbitrary properties when practical, using the installed version's supported syntax. Use small custom CSS rules for mechanisms that utilities cannot express clearly, such as `@property` or reusable keyframes. Preserve logical properties when translating; check the upstream version notes before using newer utilities.

## Design workflow

Keep the active workflow when arriving from Design. For animation design or mobile interaction decisions, read our [Design entry point](../SKILL.md) and its matching branch, reusing guidance already loaded. Route upstream references to Emil's skills through that wrapper so its exclusions and collaboration preferences still apply.

For overlapping motion recipes, inherited animation variables, animated layout properties, or mobile root scrolling, read [CSS integration](CSS_INTEGRATION.md). It defines the division of responsibility and resolves those specific conflicts.

## Compatibility and verification

Read the project's browser targets. Treat upstream `Support:` lines as revision-specific evidence and verify uncertain support against current official documentation and the target browsers. A recipe's instruction to omit a fallback assumes its basic behavior remains usable. When a required interaction would be lost, choose a compatible implementation or a deliberate fallback.

Verify the required behavior as well as appearance; native CSS and HTML mechanisms still need the component's keyboard/focus semantics and state management.

Use [good-css.com](https://good-css.com/) when an entry's appearance or interaction needs a live specimen, or its reasoning and credits need context. The site can differ from the pinned checkout; use local entries for the adopted source and target-browser checks for compatibility. Loading the whole site is unnecessary for a routine CSS edit.

## Source availability and updates

Resolve the Design wrapper's real path before following relative links. Keep the upstream checkout at its based-on commit in [UPSTREAM.md](../../../UPSTREAM.md), with source skills outside the installed wrapper. If it is missing or at a different revision, report that condition rather than changing the pin or silently substituting another installed skill.

Fetch updates without advancing the checkout. Adopt a revision after reviewing its relevant changes, then advance the clean checkout and based-on record together. See [provenance](../PROVENANCE.md).
