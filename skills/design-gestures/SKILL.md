---
name: design-gestures
description: "Build and polish web drag, swipe, snap, dismiss, and hold interactions with direct tracking, velocity-aware release, and interruption."
---

# Gestures

Read the [source rules](../design/references/SOURCES.md) once, reusing them if already loaded. Then follow the upstream [gestures](../../repos/emil/skills/gestures/SKILL.md) for the requested task; local adaptations below take precedence.

## Task and Codex adaptations

Inspect the existing gesture and scrolling contract before choosing an implementation. Reuse accessible project primitives and dependencies for sheets and drawers; do not invoke the excluded library-selection skill or introduce a dependency without a task-specific reason. Preserve direct pointer tracking, velocity-aware release, interruption, and reduced-motion behavior from upstream. Verify cancellation, repeated gestures, interactive children, keyboard alternatives, and scroll ownership relevant to the change. For phone-specific behavior, also read [design-mobile](../design-mobile/SKILL.md); desktop emulation does not establish physical-device behavior. Read [design-css](../design-css/SKILL.md) when writing styles, and use the [source map](../design/references/SOURCE_MAP.md) for upstream specialist handoffs. Stay within web scope.
