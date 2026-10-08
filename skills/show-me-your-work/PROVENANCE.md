# Source and ownership

The original [show-me-your-work skill](https://github.com/cursor/plugins/tree/d0ef80d86795816da932a153458c5dbe192d294e/pstack/skills/show-me-your-work) is used unchanged from Poteto's pinned checkout. `SKILL.md` and any bundled resource directories are relative symlinks into `repos/pstack/pstack/skills/show-me-your-work`; [LICENSE](LICENSE) links to the upstream license. Keep the collection layout intact.

Local `agents/openai.yaml` supplies Codex UI metadata and disables implicit invocation. The other personal skills retain the user's rule against routing here. There is no local workflow override; upstream environment assumptions and cross-references remain as written.

Adopt updates through the shared Poteto checkout and pin recorded in [UPSTREAM.md](../../UPSTREAM.md). The links expose the adopted revision without copying or rewriting the skill.

## Host requirements

The original workflow requires a task transcript under `agent-transcripts/` for its [transcript audit](SKILL.md#audit-the-log-against-the-transcript) and a separate reviewer from a different model family for its [cross-model review](SKILL.md#cross-model-review-of-the-trail). These capabilities depend on the host environment. When unavailable, those requirements remain unmet; a valid decision log alone does not establish a complete audit.
