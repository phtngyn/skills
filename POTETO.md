# Poteto source fidelity

The 56 retained Poteto skills are copied byte for byte from the adopted `repos/pstack/pstack/skills/` source recorded in [UPSTREAM.md](UPSTREAM.md). This includes frontmatter, invocation examples, model defaults, tool names, paths, playbooks, scripts, and references.

The only local invocation addition is `agents/openai.yaml` with `policy.allow_implicit_invocation: false` for every installed skill. No content substitutions or compatibility rewrites run during generation. Upstream instructions retain their original platform assumptions.

Excluded from installation: `make-bot-ui`, `typescript-best-practices`, and Benny. References to excluded skills remain unchanged inside retained upstream content. Effect, full-send, and full-stop are locally maintained and are outside this import.

Regenerate and verify with:

```bash
python3 scripts/port_poteto.py
python3 scripts/port_poteto.py --check
python3 scripts/validate.py
python3 tests/test_port_poteto.py
```

Regeneration removes obsolete tracked files in managed Poteto skill directories and preserves untracked notes and personal skills. The previous Codex-specific substitutions have been removed.
