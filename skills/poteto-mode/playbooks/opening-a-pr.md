### Opening a PR

Consult when a playbook reaches an authorized PR publication step.

Keep unrelated changes out. Use a task branch or the host’s worktree mechanism when appropriate. Review the diff for unexpected behavior, dead code, and redundant branches before committing.

Title: `type(scope): subject`, naming a real symbol when one carries the change. Body: a one-minute briefing under 40 lines with these `##` headings in order, dropping empty ones: `## Why`, `## What changed`, `## Scope`, `## Tradeoffs` (only rejected alternatives a reviewer would otherwise ask about), `## Blast Radius`, `## Verification`.

Stack follow-ups by base branch. Use the requested draft state. Use the host PR creation tool when exposed. Otherwise use `gh pr create` on GitHub. Follow the [host linking rules](../references/codex.md). Babysit only when requested or part of the authorized delivery workflow.
