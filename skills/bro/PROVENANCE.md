# Source and ownership

`SKILL.md` is an unchanged copy of Poteto's original [bro skill](/Users/phtngyn/Developer/skills/repos/pstack/pstack/skills/bro). A regular entry-point file allows Codex discovery without following a file symlink. [LICENSE](/Users/phtngyn/Developer/skills/repos/pstack/pstack/LICENSE) links to the upstream license.

Local `agents/openai.yaml` supplies Codex UI metadata and disables implicit invocation. There is no custom workflow. Keep upstream relative references usable from this directory.

When adopting Poteto updates in [UPSTREAM.md](../../UPSTREAM.md), refresh this copy from the adopted checkout and verify byte equality. Fetching alone must preserve the adopted contents.
