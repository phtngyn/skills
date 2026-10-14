---
name: write
description: Write and review documents agents consume, including skills, repository instructions, specs, runbooks, and reference guides. Ground claims in authoritative sources and keep conditional detail efficient to load.
---

# Write

Write for the agent reading the document. Use Matt Pocock's original authoring guidance with our source verification and freshness rules. Preserve the requested audience, scope, terminology, and requirements.

## Load the authoring guidance

Before drafting or reviewing, read upstream [Writing for Agents](/Users/phtngyn/Developer/skills/repos/mattpocock/skills/productivity/writing-for-agents/SKILL.md). Reuse it during the task and resolve references from its directory.

For a skill, also read [skill mechanics](/Users/phtngyn/Developer/skills/repos/mattpocock/skills/productivity/writing-for-agents/SKILL-MECHANICS.md). Use Codex's `skill-creator` for frontmatter and `agents/openai.yaml`; upstream mechanics explain choices across agent environments.

## Ground the document

Identify the document's job and the decisions its reader must make. Inspect the relevant project instructions, existing document, and sources for the claims being written or changed.

| Claim | Authority to inspect |
| --- | --- |
| Current behavior, APIs, commands, or configuration | The consuming project's code, exports, configuration, command help, and focused tests or observable behavior |
| Intended behavior, requirements, or policy | The user's accepted requirements and authoritative specifications or decision records |
| External APIs or standards | Official sources matching the version or standard the project uses |

Read the supporting section before citing it. When sources disagree, identify which claim each governs and report unresolved conflicts. Distinguish inference and assumptions from verified facts; confirm documented behavior against its implementation.

Cite material factual claims near the text they support. For this collection's cloned sources, use absolute filesystem links with a line or symbol locator and record reviewed revisions in provenance. Use project-relative links for project documents and version-specific official links for sources without a local clone. Link to the section or test that supports the claim. Attribute exact quotations; quote briefly when wording matters and otherwise summarize.

## Keep facts fresh

Link to authoritative files, exports, or commands for facts the reader can retrieve cheaply. Keep non-obvious rationale, constraints, and instructions at the point of action, with their source.

When a volatile fact must be repeated, identify its source and relevant version, revision, or environment. Name useful refresh triggers, such as an export rename, dependency upgrade, configuration change, or superseding decision. Citations help locate evidence; copied claims still need rechecking.

Reuse verified source locations and recheck when their contents change or evidence conflicts. Keep source checks proportional to the edit.

## Draft and verify

Apply upstream hierarchy, context pointers, completion criteria, and pruning. Preserve requirements that change behavior, remove duplication, and link conditional detail with a clear trigger. Keep instructions needed on every run in the entry point.

Check that links and locators resolve, quotations match, and cited sources support the actual claims. Verify documented commands through non-mutating or isolated checks when needed. Trace the reader's requested task through the document and confirm its prerequisites, branches, and completion conditions remain usable. Report missing source evidence and consequential limitations.

## Sources and updates

Use the linked local Matt checkout at its based-on commit in [UPSTREAM.md](../../UPSTREAM.md). If it is missing or mismatched, report the condition rather than changing the pin or substituting another installed copy. Fetching preserves the checkout; adopt a reviewed revision by advancing the checkout and based-on record together. See [provenance](PROVENANCE.md).
