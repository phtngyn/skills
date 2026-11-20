# Poteto for Codex

The 56 retained Poteto skills start from the adopted `repos/pstack/pstack/skills/` source recorded in [UPSTREAM.md](UPSTREAM.md). The generator removes Cursor-only entry point metadata, translates bundled `/skill-name` invocations to Codex’s `$skill-name` syntax, and writes explicit-only policy in `agents/openai.yaml`. It then applies [the Codex port](scripts/poteto-codex.patch) to the normalized source for workflow-specific changes. Other files retain their upstream bytes.

Use `$skill-name` in chat. The [runtime guidance](skills/poteto-mode/references/codex.md) covers Codex delegation, history, verification, and PR lifecycles, including T3 tools where available. Agents inherit the active Codex model by default. `$setup-pstack` can set optional role preferences supported by the host.

The imported catalog excludes `make-bot-ui` and `typescript-best-practices`. Effect, full-send, and full-stop are maintained separately.

Regenerate and verify with:

```bash
python3 scripts/port_poteto.py
python3 scripts/port_poteto.py --check
python3 scripts/validate.py
python3 tests/test_port_poteto.py
```

When adopting a new pin, review the upstream changes for host assumptions and refresh the patch against that checkout. Review new skills, playbooks, and helpers even if the patch still applies. A patch conflict stops regeneration before it writes to the collection. Regeneration removes obsolete tracked files in managed Poteto directories and preserves untracked notes and personal skills.
