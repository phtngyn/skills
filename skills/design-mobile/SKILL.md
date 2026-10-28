---
name: design-mobile
description: "Polish mobile web viewport, touch, scrolling, safe areas, keyboard, and browser behavior."
---

# Mobile web

Read the [source rules](../design/references/SOURCES.md) once, reusing them if already loaded. Then follow the upstream [mobile-native](/Users/phtngyn/Developer/skills/repos/emil/skills/mobile-native/SKILL.md) for the requested task; local adaptations below take precedence.

## Task and Codex adaptations

Inspect the page's scrolling and gesture contract before applying platform fixes. Reuse capability media queries and native CSS rather than device sniffing. Verify keyboard, safe areas, browser navigation, scrolling, and gesture interruption relevant to the change. Use physical-device evidence for phone-specific claims; desktop emulation can show responsive layout but leaves device behavior unverified. For CSS changes, read [design-css](../design-css/SKILL.md), including the shared root-scrolling integration rules. Stay within web scope.
