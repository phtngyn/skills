# Poteto for Codex

The 54 Poteto skill directories in `skills/` derive from the pinned `repos/pstack/pstack/skills/` source recorded in [UPSTREAM.md](UPSTREAM.md). Every upstream core skill is included except `make-bot-ui`, `typescript-best-practices`, `create-formal-verification-skill`, and `maintain-formal-verification-skill`. Benny's automation pack is excluded. `design` and `effect` are retained personal skills. Retired skills are removed rather than kept as aliases.

## Adaptation

The upstream checkout remains unchanged. Installed skill directories contain local copies, including referenced resources and helpers. Symlinked upstream resources are materialized, so installed instructions do not accidentally edit upstream files.

- Preserve original skill identities and the 24 principles. Convert command examples to `$skill-name`.
- Translate upstream manual-only policy into `agents/openai.yaml` with `allow_implicit_invocation: false`. Remove unsupported Cursor frontmatter fields.
- Replace Cursor-specific agent calls and hardcoded provider models with the [Codex runtime contract](skills/poteto-mode/references/codex.md). Inheritance is the default. `$setup-pstack` records optional pstack role preferences without modifying native Codex configuration.
- Use portable comment-review instructions rather than require a preinstalled specialized agent. Distinguish independent contexts from actual model diversity.
- Replace private transcript-layout assumptions with supported host history, identified transcripts, and explicit partial-history fallbacks.
- Port the 23 playbooks to available Codex tools. Persistent hooks, Custom Modes, Cursor scheduling, plugin installation, and automatic external-write permissions are not carried over. Planning produces a plan; PR delivery applies when requested.
- Retain portable orchestration and GitHub watcher helpers. Remove unused plan-template and Cursor transcript-audit helpers. The retained Bun tools use their frozen dependency lock.

## Adopted refresh

On 2026-10-26, the port adopted `99b609a72323b70204eab407c622f436e858e112` (pstack 0.15.32). Added explicit-only `ketchup-video`, which follows ketchup and renders an evidence-based silent slide video with pending decisions as text. Statechart now covers product flows, protocols, services, and designs, with the Pele PNG renderer, reduced overview coverage, goal paths, and clearer model evidence and counterexample handoffs. Its reachable scripts and fixtures are refreshed; removed upstream model fixtures are removed locally too. The command path in its entry point is corrected.

Portable helpers now prefer active PRs over branch history, distinguish fork heads during stack discovery, and cap polling sleeps at the deadline. Reflect routes edits out of plugin caches to maintained sources or approved writable copies. Existing swarm wording already covers the upstream numbering and report correction. The unused plan checker and Cursor transcript audit remain excluded, as do formal-verification generators and Claude packaging. The collection contains 56 skills.

Validation passed: collection and skill metadata checks, seven validator tests, nineteen installer tests, 75 Bun helper tests, strict helper typechecking, and installed-link/source-pin checks. Statechart passed 57 tests, including renderer checks; 93 TLC-dependent tests were skipped because TLC is unavailable. Full model-checking remains unverified. Bun checks ran through `npx bun` because Bun is not installed globally.

On 2026-10-23, the port adopted `8b3326d99fd4b993cb33a24dad8af03175c642c5` (pstack 0.15.28). The standalone `statechart` skill and its reachable scripts, model, and test fixtures are included with explicit-only Codex invocation. It requires Java and TLC for model checking, and a Mermaid renderer for PNG output; the command documents missing prerequisites. `sharpen` now returns a rewritten prompt rather than executing the task, preserving explicit user constraints and scope. Help, recipes, and the catalog reflect that behavior.

The formal-verification creation exclusion is preserved and its new maintenance companion is excluded too. Setup offers and help routes to those excluded skills, Cursor/Claude packaging, and upstream guide-only changes are not imported. Statechart validation passed 29 tests; 38 TLC-dependent tests were skipped because TLC is unavailable. Full model-checking and PNG rendering were not exercised. No existing playbooks, principles, or orchestration helpers changed upstream. That revision contained 55 entries.

On 2026-10-18, the port adopted `4382e687a50b8d2c5ce4d141d001186589cff8d5` (still labeled pstack 0.15.25). The upstream formal verification skill was reviewed and excluded at the user's request.

Ketchup lists every pending decision and every item covered by a shared decision, with evidence and risk. Completeness takes precedence over a word target. Existing visual guidance and authorization boundaries remain. Collection validation now checks README coverage and counts, root documentation links, Markdown heading anchors, and titled links. Upstream's name fixes are already covered locally, and its autopilot documentation correction already matches this port. Claude Code packaging and Cursor-specific validation are excluded. Playbooks, principles apart from the retired-skill pointer, helpers, and dependencies are unchanged.

The user retired `typescript-best-practices` and declined `create-formal-verification-skill`; their installed links and routing references are removed. That revision contained 54 entries. Upstream's absolute rule requiring type guards for every brand is not imported.

On 2026-10-17, the port adopted pstack 0.15.25 at `101b274dd991f694e1f7024be2157e5f3adf07de`. The refresh adds explicit-only `sharpen`, generalizes premise testing and idempotency, distinguishes legitimate defensive handling from symptom suppression, and judges tests by observable behavior and refactor tolerance. Principle summaries and `correct` follow those changes.

Catch-up reporting uses existing visual evidence when it explains the change, with concise prose and plain action items. Fixed box counts and mandatory visual comparisons are removed. Autopilot reports use that guidance without granting monitoring, merge or publication authority. `sharpen` preserves explicit user constraints and task scope.

The type-system and caller-migration skills retain their concrete guidance despite upstream pruning. Review judgment retains useful context and removes the arbitrary five-finding limit. Swarm keeps its Codex adaptation, including explicit worker count and missing-coverage handling; upstream's redundant prose cuts require no additional mechanism here. Claude Code packaging and harness mappings are excluded. The portable helper implementations and dependencies are unchanged. Wording review also aligns model inheritance and writer isolation with the runtime contract, preserves evidence-based uncertainty, and distinguishes trusted input types from changing runtime state. TypeScript guidance uses established brand conventions, explains assertions and `satisfies` accurately, and avoids claiming that a plain numeric duration prevents negative ranges.

## Reference reviewed

[Aqua-123/pstack-for-codex](https://github.com/Aqua-123/pstack-for-codex/tree/3d2770d638d8fb9eabd85c977fe76d90e6b426ce) was reviewed on 2026-10-15, especially its README, Codex adaptation notes, runtime contract, Poteto Mode, Why, and portable comment reviewer. It informed inherited models, isolated writers, capability fallbacks, and explicit distinction between a current task and persistent monitoring. This collection does not import that repository's plugin packaging, hooks, optional profiles, compatibility machinery, or Benny pack.

Codex metadata and runtime documentation were reviewed at [Build skills](https://learn.chatgpt.com/docs/build-skills) and [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). Recheck these when skill discovery or runtime agent schemas change.

## Refresh

Fetch upstream without changing its adopted pin. Review changes to every included entry point and its reachable resources against this port, then advance the clean checkout and based-on record together. Preserve Codex runtime adaptations. Run collection validation, isolated installer tests, and the Bun helper suite before adopting changed helpers. Reinstall and check the global links after the catalog changes. Source existence alone does not prove a local adaptation is current.
