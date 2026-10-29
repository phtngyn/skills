# Poteto source and port

The 54 Poteto skill directories derive from the pinned `repos/pstack/pstack/skills/` source in [UPSTREAM.md](UPSTREAM.md). The upstream checkout stays unchanged. The installed files retain upstream workflows, principles, prompts, and supporting tools rather than locally shortened versions.

## Compatibility changes

The reproducible substitutions live in [port_poteto.py](scripts/port_poteto.py), outside the installed skill prompts:

- Convert `/skill-name` examples to `$skill-name`, remove unsupported frontmatter, and preserve invocation policy in `agents/openai.yaml`.
- Replace unavailable agent/tool fields and provider-only model defaults with native calls and the existing per-role model choices. Unconfigured roles inherit. The role names, panel sizes, and workflow stages stay intact.
- Map project skill locations, skill authoring, source references, and runtime verification to their local equivalents.
- Use supported host history or explicitly identified transcripts instead of Cursor-private paths. The worktree audit accepts an optional `PSTACK_TRANSCRIPTS` directory.
- Preserve Comment Sicko's original persona as a task-specific reference. It replaces the earlier rewritten comment-review contract.

There is no shared Codex runtime manual or mandatory read explaining how to use Codex. Platform-specific steps still depend on the capabilities actually available in the host.

## Retained exclusions

User exclusions remain `make-bot-ui`, `typescript-best-practices`, `create-formal-verification-skill`, `maintain-formal-verification-skill`, and Benny. References that would activate those excluded skills are removed. Design and Effect remain separate personal skills; Poteto does not route to Design.

## Other ports reviewed

Reviewed on 2026-10-27: [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude/blob/main/plugins/pstack/skills/poteto-mode/references/codex-tools.md) separates shared workflows from tool mappings. [mdsmithaustin/pstack](https://github.com/mdsmithaustin/pstack/blob/main/PORTING.md) records systematic substitutions and treats upstream as the workflow source of truth. This collection applies the required substitutions during generation rather than loading another mapping manual at runtime. No other port's policy forks, hooks, native profiles, or model defaults are imported.

## Adopted refresh

On 2026-10-29, adopted pstack 0.15.36 at `1ba91fc25c0977741dd0e267849e6234b037ed0a`. The statechart compiler and tests replace the older helpers, Interrogate keeps only executed and reverified findings, and Orchestrate no longer uses its script store. Arena requires a judge from another model family or reports that judging was skipped. Upstream workflows and resources remain intact apart from the compatibility substitutions above. Regeneration removes obsolete tracked files in the managed Poteto skill directories and preserves untracked notes and personal skills.

Validation passed 61 Bun helper tests and the watcher typecheck. The unchanged statechart suite passed 267 tests with 67 live TLC tests skipped without Java/TLC configuration. On this macOS host, its symlink launcher fixture needs a canonical temporary directory (`TMPDIR=/private/tmp npm test`); the default `/var/folders` path resolves under `/private/var/folders` and makes the fixture's relative link miss its target. No upstream code or tests were changed for that environment issue.

## Refresh and verify

Review upstream changes before advancing the clean checkout and based-on pin together. Then run:

```bash
python3 scripts/port_poteto.py
python3 scripts/port_poteto.py --check
python3 scripts/validate.py
python3 tests/test_validate.py
python3 tests/test_port_poteto.py
python3 tests/test_setup.py
./scripts/setup.sh --check
```

The check reports drift without writing. When imported helpers change, also run their Bun tests and typecheck as documented in [README.md](README.md#validation).
