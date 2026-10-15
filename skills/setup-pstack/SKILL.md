---
name: setup-pstack
description: "Configure pstack role and panel preferences for Codex using available models, reasoning controls, and inherited defaults."
---

# Set up pstack for Codex

Configure model preferences for pstack roles without changing Codex's global settings.

1. Read the [Codex delegation contract](../poteto-mode/references/codex.md). Inspect the active agent tool's schema and any runtime-provided model choices. Treat those as the available set. If overrides are unavailable, retain inheritance and explain the limitation.
2. Read `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json` if it exists. Missing configuration means every role inherits the current model. Do not mine authentication files or guess model identifiers.
3. Use the available user-input tool to ask which roles to change when the request does not specify them. Offer inheritance first, then only supported model choices. Ask about reasoning effort only when the runtime supports it. Preserve unspecified choices on updates.
4. Write the JSON file with one object per role. A scalar role has `model: "inherit-parent"` or a supported model identifier, with optional `reasoning_effort`. A panel role has a list of these objects. Default panels have two inherited entries. The cross-judge pool selects one entry rather than launching the whole list.
5. Validate the JSON by parsing it, then show the effective choices and the file path. This is a pstack convention read by these skills, not a native Codex configuration key. It applies when a skill next reads it. Do not claim it changes a running agent's model.

Supported role names:

- `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `hardest tasks`, `judgment and prose`
- `how explorer`, `how explainer`, `why investigators`, `why synthesizer`
- `reflect tooling`, `reflect judgment, divergent, synthesizer`
- Panel roles: `arena runners`, `architect runners`, `interrogate reviewers`
- Pool role: `arena cross-judge pool`
- `swarm workers`

Example:

```json
{
  "roles": {
    "arena runners": [{"model": "inherit-parent"}, {"model": "inherit-parent"}],
    "swarm workers": {"model": "inherit-parent"}
  }
}
```

Only pass fields the active agent tool accepts. A rejected configured override falls back once to inheritance, with an explicit report. Never manufacture a replacement model or reasoning level.
