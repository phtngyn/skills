# Personal skills for Codex

68 skills: the 54 Poteto core skills retained after excluding `make-bot-ui`, `typescript-best-practices`, `create-formal-verification-skill`, and `maintain-formal-verification-skill`, an independent Design family with a coordinator and twelve subskills, and `effect`. Benny is excluded. The former `build`, `prompt`, and `write` wrappers are removed; `bro` and `ketchup` now belong to the adapted Poteto collection.

## Install

Keep this repository in a permanent location, then run:

```bash
./scripts/setup.sh
./scripts/setup.sh --check
```

Setup clones missing upstream sources and moves clean existing checkouts to the adopted revisions in [UPSTREAM.md](UPSTREAM.md), fetching missing commits only when needed. It then links each skill into `~/.agents/skills`. Local source edits stop setup with repair guidance; branch pointers are never rewritten. Retired links owned by this collection are removed after preflight succeeds. Foreign links and real directories are preserved; a conflicting current skill name stops installation before changing links.

On each machine, update with:

```bash
git pull --ff-only
./scripts/setup.sh
```

Setup follows this collection’s reviewed pins, not upstream’s latest development branches. Rerunning it at the current pins needs no fetch. `--check` only reports drift; running setup repairs clean revision mismatches. If you edit a source under `repos/`, commit, stash, or move those edits before updating.

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

`poteto-mode` coordinates engineering work through its own skills, principles, and playbooks. Invoke `$design` separately for UI work through its own Design specialists and shared workflow. Either family works without loading the other, and Poteto does not invoke Design. The 23 playbooks under `skills/poteto-mode/playbooks/` remain ordinary resources, not extra registered skills. `$effect` supplies decisions for the latest stable Effect release.

## Skills

### Poteto

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
| `ketchup-video` | Catch up through a short silent video, with pending decisions as text. |
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
| `statechart` | Draw model-backed charts of product flows, protocols, and services and turn agreed charts into TLA+ skeletons. |
| `no-comments` | Review comments and address accepted clutter or unenforced constraints. |
| `correct` | Prevent recurring agent mistakes structurally. |
| `technical-writing` | Structure and edit technical documents. |
| `unslop` | Remove formulaic AI prose. |
| `automate-me` | Capture personal working conventions in a mode skill. |
| `reflect` | Turn repeated session lessons into authorized skill improvements. |
| `setup-pstack` | Configure optional model preferences for Codex delegation roles. |

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

### Design

Invoke `$design` to coordinate the task, or invoke a specialist directly. All Design entries are explicit-only. The specialists share Design's own workflow and source rules and read their detailed guidance from the pinned Emil and Good CSS sources. See [Design ownership](skills/design/PROVENANCE.md).

| Skill | Purpose |
| --- | --- |
| `design` | Coordinate UI work through the Design specialists. |
| `design-ui` | Implement or critique interface craft, components, and interaction states. |
| `design-css` | Implement and review layout, typography, overflow, and native CSS. |
| `design-prototype` | Build distinct UI directions in an interactive picker. |
| `design-animate` | Build purposeful, interruptible web motion. |
| `design-animation-performance` | Diagnose frame drops and animation rendering costs. |
| `design-review-animations` | Review a motion component or diff without editing. |
| `design-improve-animations` | Audit product motion and prepare scoped execution plans. |
| `design-find-animation-opportunities` | Find justified opportunities for motion without editing. |
| `design-animation-vocabulary` | Identify and explain an animation effect. |
| `design-apple` | Shape physical, Apple-inspired web interactions. |
| `design-mobile` | Polish mobile web touch, viewport, scrolling, and safe areas. |
| `design-break-ui` | Stress interfaces with difficult realistic data. |

### Effect

| Skill | Purpose |
| --- | --- |
| `effect` | Design, implement, and review programs and libraries with the latest stable Effect release. |

## Source fidelity

Poteto's retained skills are regenerated from the pinned upstream source by `scripts/port_poteto.py`. The port changes invocation metadata, unavailable tool calls, model configuration, and platform paths. It adds no runtime manual. [POTETO.md](POTETO.md) records those substitutions and exclusions; [UPSTREAM.md](UPSTREAM.md) records source pins.

Design is an independent family with its own [source rules](skills/design/references/SOURCES.md). [Effect research](research/effect/MAINTENANCE.md) stays outside the installed skills.

## Validation

```bash
python3 scripts/port_poteto.py --check
python3 scripts/validate.py
python3 tests/test_validate.py
python3 tests/test_port_poteto.py
python3 tests/test_setup.py
./scripts/setup.sh --check
```

Collection validation checks the included catalog, invocation policy, README coverage, stated catalog counts, local Markdown links and heading anchors, and the absence of Design dependencies on Poteto skills. Validator tests exercise documentation failures in temporary fixtures. Installer tests use temporary directories and local Git fixtures, with no changes to global skills and no network fetching.

The imported orchestration and GitHub watcher helpers require Bun. When changing those helpers, run from `skills/poteto-mode/scripts`:

```bash
bun install --frozen-lockfile
bun test orch watch-pr check-plan.test.ts
bun run typecheck
```

Without Bun, skills use their documented direct-tool fallback. The helpers are not required for skill installation or discovery.
