---
name: write
description: Write and review documents agents consume, including skills, repository instructions, specs, runbooks, and reference guides. Ground claims in authoritative sources and keep conditional detail efficient to load.
---

# Write

Write for the agent reading the document. Use Matt Pocock's original authoring guidance with our source verification and freshness rules. Preserve the requested audience, scope, terminology, and requirements.

## Load the authoring guidance

Read the upstream [Writing for Agents](../../repos/mattpocock/skills/productivity/writing-for-agents/SKILL.md) before drafting or reviewing. Reuse it during the task. Resolve its references from that upstream directory.

When the document is a skill, also read its [skill mechanics](../../repos/mattpocock/skills/productivity/writing-for-agents/SKILL-MECHANICS.md). For Codex packaging, use the available `skill-creator` guidance for actual frontmatter and `agents/openai.yaml`; the upstream mechanics explain conceptual choices across agent environments.

## Ground the document

Identify the document's job and the decisions its reader must make. Inspect the relevant project instructions, existing document, and sources for the claims being written or changed.

| Claim | Authority to inspect |
| --- | --- |
| Current behavior, APIs, commands, or configuration | The consuming project's code, exports, configuration, command help, and focused tests or observable behavior |
| Intended behavior, requirements, or policy | The user's accepted requirements and authoritative specifications or decision records |
| External APIs or standards | Official sources matching the version or standard the project uses |

Read the supporting section before citing it. When sources disagree, establish which claim each governs and report unresolved conflicts. Keep inferred explanations and unverified assumptions distinct from established facts; an existing document alone is not proof of current implementation behavior.

Cite material factual claims near the text they support, grouping related claims when appropriate. Prefer stable repository-relative links with a heading or symbol locator. Use immutable revision links for historical snapshots and version-specific external links when available. Attribute exact quotations; quote briefly when precise wording matters and otherwise summarize. A repository homepage or unrelated test does not substantiate a specific behavior claim.

## Keep facts fresh

Prefer a pointer to the authoritative file, export, or command over copying information the reader can retrieve cheaply. Keep non-obvious rationale, constraints, and instructions the reader needs at the point of action in the document, with their source.

When a volatile fact must be repeated, identify its canonical source and the relevant version, revision, or environment. Name the change that should trigger rechecking it when that is useful: a renamed export, dependency upgrade, configuration change, or superseding decision. A citation helps locate the truth; it does not establish that a copied claim is still current.

Reuse verified source locations during the task. Recheck when the underlying source changes or conflicting evidence appears. A small edit needs focused source checks, not a survey of the whole repository.

## Draft and verify

Apply the upstream hierarchy, context pointers, completion criteria, and pruning to the draft. Preserve behavior-changing requirements while removing duplicated facts and instructions that add no useful guidance. Reach conditional detail through a pointer that states when it is needed; keep shared instructions immediately available.

Check that links and locators resolve, quotations match, and cited sources support the actual claims. Verify documented commands through non-mutating or isolated checks when needed. Trace the reader's requested task through the document and confirm its prerequisites, branches, and completion conditions remain usable. Report missing source evidence and consequential limitations.

## Sources and updates

Resolve this wrapper's real directory before following source links. The Matt checkout must match its based-on commit in [UPSTREAM.md](../../UPSTREAM.md). If it is missing or mismatched, report the condition rather than changing the pin or substituting another installed copy. Fetching preserves the checkout; adopt a reviewed revision by advancing the checkout and based-on record together. See [provenance](PROVENANCE.md).

## User-only companion commands

Do not invoke or route to `bro` or `show-me-your-work`, including through upstream references. Only the user can activate those standalone skills explicitly. Continue the current workflow without them.
