# Source and ownership

The original [show-me-your-work skill](https://github.com/cursor/plugins/tree/d0ef80d86795816da932a153458c5dbe192d294e/pstack/skills/show-me-your-work) remains unchanged in Poteto's pinned checkout. Our local `SKILL.md` loads it directly; bundled `scripts` and `references` remain relative symlinks into `repos/pstack/pstack/skills/show-me-your-work`. [LICENSE](LICENSE) links to the upstream license. Keep the collection layout intact.

Local `agents/openai.yaml` enables automatic selection. The entry point adds the user's preference for selective activation on substantial work, a separate subagent reviewer, and honest host fallbacks. Its own description supplies selection conditions; other skills need no routing instructions. Bro remains user-only. These integration choices are personal additions, not Poteto's original instructions.

Adopt updates through the shared Poteto checkout and pin recorded in [UPSTREAM.md](../../UPSTREAM.md). Review the relevant source changes against the local integration rules when adopting a revision; the upstream workflow is referenced rather than copied.

## Host requirements

The original workflow requires a task transcript under `agent-transcripts/` for its [transcript audit](../../repos/pstack/pstack/skills/show-me-your-work/SKILL.md#audit-the-log-against-the-transcript) and a separate reviewer from a different model family for its [cross-model review](../../repos/pstack/pstack/skills/show-me-your-work/SKILL.md#cross-model-review-of-the-trail). These capabilities depend on the host environment. The local entry point permits review of available task evidence and a separate agent using the inherited model, while explicitly identifying unmet transcript and cross-family requirements. These fallbacks provide useful review without claiming a complete upstream audit.
