# Poteto for Codex

The 53 Poteto skill directories in `skills/` derive from the pinned `repos/pstack/pstack/skills/` source recorded in [UPSTREAM.md](UPSTREAM.md). Every upstream core skill is included except `make-bot-ui`. Benny's automation pack is excluded. `design` and `effect` are retained personal skills. Retired wrappers are removed rather than kept as aliases.

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

On 2026-10-17, the port adopted pstack 0.15.25 at `101b274dd991f694e1f7024be2157e5f3adf07de`. The refresh adds explicit-only `sharpen`, generalizes premise testing and idempotency, distinguishes legitimate defensive handling from symptom suppression, and judges tests by observable behavior and refactor tolerance. Principle summaries and `correct` follow those changes.

Catch-up reporting uses existing visual evidence when it explains the change, with concise prose and plain action items. Fixed box counts and mandatory visual comparisons are removed. Autopilot reports use that guidance without granting monitoring, merge or publication authority. `sharpen` preserves explicit user constraints and task scope.

The type-system and caller-migration skills retain their concrete guidance despite upstream pruning. Review judgment retains useful context and removes the arbitrary five-finding limit. Swarm keeps its Codex adaptation, including explicit worker count and missing-coverage handling; upstream's redundant prose cuts require no additional mechanism here. Claude Code packaging and harness mappings are excluded. The portable helper implementations and dependencies are unchanged. Wording review also aligns model inheritance and writer isolation with the runtime contract, preserves evidence-based uncertainty, and distinguishes trusted input types from changing runtime state. TypeScript guidance uses established brand conventions, explains assertions and `satisfies` accurately, and avoids claiming that a plain numeric duration prevents negative ranges.

## Reference reviewed

[Aqua-123/pstack-for-codex](https://github.com/Aqua-123/pstack-for-codex/tree/3d2770d638d8fb9eabd85c977fe76d90e6b426ce) was reviewed on 2026-10-15, especially its README, Codex adaptation notes, runtime contract, Poteto Mode, Why, and portable comment reviewer. It informed inherited models, isolated writers, capability fallbacks, and explicit distinction between a current task and persistent monitoring. This collection does not import that repository's plugin packaging, hooks, optional profiles, compatibility machinery, or Benny pack.

Codex metadata and runtime documentation were reviewed at [Build skills](https://learn.chatgpt.com/docs/build-skills) and [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). Recheck these when skill discovery or runtime agent schemas change.

## Refresh

Fetch upstream without changing its adopted pin. Review changes to every included entry point and its reachable resources against this port, then advance the clean checkout and based-on record together. Preserve Codex runtime adaptations. Run collection validation, isolated installer tests, and the Bun helper suite before adopting changed helpers. Reinstall and check the global links after the catalog changes. Source existence alone does not prove a local adaptation is current.
