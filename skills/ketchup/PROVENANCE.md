# Source and ownership

`SKILL.md` is an unchanged copy of Poteto's original [ketchup skill](https://github.com/cursor/plugins/tree/1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def/pstack/skills/ketchup). A regular entry-point file allows Codex discovery without following a file symlink. [LICENSE](LICENSE) links to the upstream license.

Local `agents/openai.yaml` supplies Codex UI metadata and disables implicit invocation. There is no custom workflow. Keep upstream relative references usable from this directory.

When adopting Poteto updates in [UPSTREAM.md](../../UPSTREAM.md), refresh this copy from the adopted checkout and verify byte equality. Fetching alone must preserve the adopted contents.
