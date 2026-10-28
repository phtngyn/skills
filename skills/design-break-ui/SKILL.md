---
name: design-break-ui
description: "Exercise interfaces with difficult realistic data, compare normal and stress states, and report failures before fixes."
---

# Stress UI

Read the [source rules](../design/references/SOURCES.md) once, reusing them if already loaded. Then follow the upstream [break-ui](/Users/phtngyn/Developer/skills/repos/emil/skills/break-ui/SKILL.md) for the requested task; local adaptations below take precedence.

## Task and Codex adaptations

Read CATALOG.md and follow the upstream normal/stress toggle workflow. Use realistic worst cases and protect real data: keep fixtures and the toggle in an isolated test or prototype surface. An audit request permits the bounded test artifact, not production data mutations or fixes. For a report-only request with no edits, inspect available fixtures or evidence instead and label unexercised cases. Verify the affected widths and interactions, report what failed, and stop. Apply fixes only when requested; then repeat the same stress cases.
