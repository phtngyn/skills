# Personal skills for Codex

55 skills: the 53 Poteto core skills retained after excluding `make-bot-ui`, `typescript-best-practices`, `create-formal-verification-skill`, and `maintain-formal-verification-skill`, plus the personal `design` and `effect` skills. Benny is excluded. The former `build`, `prompt`, and `write` wrappers are removed; `bro` and `ketchup` now belong to the adapted Poteto collection.

## Install

Keep this repository in a permanent location, then run:

```bash
./scripts/setup.sh
./scripts/setup.sh --check
```

Setup clones missing upstream sources at the adopted revisions in [UPSTREAM.md](UPSTREAM.md), verifies existing checkouts, and links each skill into `~/.agents/skills`. Existing sources are never fetched, advanced, or reset during setup. Retired links owned by this collection are removed after preflight succeeds. Foreign links and real directories are preserved; a conflicting current skill name stops installation before changing links.

Start a new chat after installation so Codex reloads the skill catalog. Invoke skills with `$skill-name`. Most Poteto skills are explicit-only, preserving upstream policy; `setup-pstack` can also be selected automatically. Workflows read sibling skill instructions when their phases need them. The retained specialists keep their invocation settings.

```bash
./scripts/setup.sh --target /path/to/isolated-skills
./scripts/setup.sh --uninstall
```

Uninstall removes only this collection's links, including retired ones. It preserves upstream checkouts and unrelated skills. Moving or deleting this repository breaks installed links.

## Workflow

Use `$poteto-mode <task>` as the general execution entry point. It chooses a playbook and applies relevant principles. Use a narrower skill when that is the whole task.

```text
$poteto-mode fix this retry path creating duplicate rows. Reproduce it, fix the root cause, and verify retries leave one row.
$architect with checkpoint redesign this importer around its callers and failure contract.
$how explain resource ownership and shutdown in this subsystem.
$interrogate review this branch against the accepted requirements without editing.
$design improve this dialog's layout and keyboard interactions.
$effect review this worker's interruption, retries, and resource lifetime.
```

A typical flow is goal clarification, system understanding, design when needed, implementation, real verification, and review. `poteto-mode` connects those phases. `design` supplies UI craft; `effect` supplies decisions for the latest stable Effect release. The 23 playbooks under `skills/poteto-mode/playbooks/` remain ordinary resources, not extra registered skills.

## Skills

| Skill | Purpose |
| --- | --- |
| `poteto-mode` | Execute substantial engineering tasks through matching playbooks. |
| `poteto-help` | Choose a workflow or prepare a concrete task prompt. |
| `in-your-own-words` | Confirm the intended goal and problem. |
| `sharpen` | Deepen a task and return a rewritten prompt without executing it. |
| `how` | Explain current architecture, ownership, and runtime flow. |
| `why` | Investigate design rationale with cited evidence and explicit uncertainty. |
| `teach` | Combine mechanics and rationale into a clear explanation. |
| `recall` | Reconstruct recent project context from available history and live state. |
| `ketchup` | Catch up on progress and every pending decision within the current chat. |
| `bro` | Restate the last response plainly. |
| `architect` | Compare interface and module designs before implementation. |
| `figure-it-out` | Design and execute an auditable workflow for ambitious unfamiliar work. |
| `arena` | Compare isolated candidates and synthesize the strongest solution. |
| `swarm` | Cover independent slices or races and aggregate evidence. |
| `show-me-your-work` | Keep a reviewable decision trail. |
| `interrogate` | Run independent adversarial review and synthesize a verdict. |
| `blast-radius` | Find downstream breakage and prove critical assumptions. |
| `benchmark-checklist` | Validate performance measurements before acting on them. |
| `tdd` | Add a focused failing regression test where a practical test path exists. |
| `create-verification-skill` | Generate and execute a project-specific real-app verification workflow. |
| `maintain-verification-skill` | Audit a verification skill and feature map against source and live behavior. |
| `statechart` | Draw model-backed charts of user-visible behavior and turn agreed charts into TLA+ skeletons. |
| `no-comments` | Review comments and address accepted clutter or unenforced constraints. |
| `correct` | Prevent recurring agent mistakes structurally. |
| `technical-writing` | Structure and edit technical documents. |
| `unslop` | Remove formulaic AI prose. |
| `automate-me` | Capture personal working conventions in a mode skill. |
| `reflect` | Turn repeated session lessons into authorized skill improvements. |
| `setup-pstack` | Configure optional model preferences for Codex delegation roles. |
| `design` | UI craft, CSS, prototyping, motion, critique, and mobile web polish using Emil and Good CSS. |
| `effect` | Design, implement, and review programs and libraries with the latest stable Effect release. |

The remaining 24 skills are principles, each prefixed with `principle-`:

- `attack-the-premise`
- `boundary-discipline`
- `build-the-lever`
- `encode-lessons-in-structure`
- `exhaust-the-design-space`
- `experience-first`
- `explain-the-number`
- `fix-root-causes`
- `foundational-thinking`
- `guard-the-context-window`
- `laziness-protocol`
- `make-operations-idempotent`
- `migrate-callers-then-delete-legacy-apis`
- `minimize-reader-load`
- `model-the-domain`
- `never-block-on-the-human`
- `outcome-oriented-execution`
- `prove-it-works`
- `redesign-from-first-principles`
- `separate-before-serializing-shared-state`
- `sequence-verifiable-units`
- `subtract-before-you-add`
- `test-behavior-not-implementation`
- `type-system-discipline`

## Codex adaptation

[The runtime contract](skills/poteto-mode/references/codex.md) defines delegation, model inheritance, writable isolation, history access, missing-capability fallbacks, and long-running work. It uses tools actually exposed by the current Codex host. It does not require Cursor, custom agent profiles, hooks, or a plugin marketplace.

All roles inherit the current model by default. `$setup-pstack` can record optional role preferences at `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json`; that file is this collection's convention rather than a native Codex configuration setting. Unavailable model overrides fall back explicitly. Independent contexts are not represented as model diversity.

History comes from supported host tools, identified transcripts, or the visible conversation. Missing history is reported. Persistent monitoring requires an explicitly requested and supported mechanism. Available browser, app-control, shell, and project verification tools provide live proof; absent proof stays unverified.

[POTETO.md](POTETO.md) records adaptation decisions and the reviewed [Aqua-123 Codex port](https://github.com/Aqua-123/pstack-for-codex/tree/3d2770d638d8fb9eabd85c977fe76d90e6b426ce). [UPSTREAM.md](UPSTREAM.md) records source pins and maintenance. [Effect research](research/effect/MAINTENANCE.md) retains historical studies and preferences outside the installed skill; application research clones are optional.

## Validation

```bash
python3 scripts/validate.py
python3 tests/test_validate.py
python3 tests/test_setup.py
./scripts/setup.sh --check
```

Collection validation checks the included catalog, invocation policy, README coverage, stated catalog counts, and local Markdown links and heading anchors. Validator tests exercise documentation failures in temporary fixtures. Installer tests use temporary directories and local Git fixtures, with no changes to global skills and no network fetching.

The imported orchestration and GitHub watcher helpers require Bun. When changing those helpers, run from `skills/poteto-mode/scripts`:

```bash
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

Without Bun, skills use their documented direct-tool fallback. The helpers are not required for skill installation or discovery.
