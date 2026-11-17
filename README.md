# Personal skills for Codex

77 skills: the 56 Poteto core skills retained after excluding `make-bot-ui` and `typescript-best-practices`, sixteen Emil skills under their original names, `effect`, two personal pstack delivery entry points, Stageshow, and Cursor Team Kit’s `deslop`. Benny is excluded. The former `build`, `prompt`, and `write` wrappers are removed; `bro` and `ketchup` now belong to the adapted Poteto collection.

## Install

Keep this repository in a permanent location, then run:

```bash
./scripts/setup.sh
./scripts/setup.sh --check
```

The global Codex instructions are saved in [global/AGENTS.md](global/AGENTS.md). Install them on a new machine alongside the skills:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}"
cp -i global/AGENTS.md "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
```

`cp -i` asks before replacing existing instructions. This installs a copy; rerun it after updating the saved instructions. The skill setup and uninstall commands manage only skills.

Setup clones missing upstream sources and moves clean existing checkouts to the adopted revisions in [UPSTREAM.md](UPSTREAM.md), fetching missing commits only when needed. It then links each skill into `~/.agents/skills`. Local source edits stop setup with repair guidance; branch pointers are never rewritten. Retired links owned by this collection are removed after preflight succeeds. Foreign links and real directories are preserved; a conflicting current skill name stops installation before changing links.

On each machine, update with:

```bash
git pull --ff-only
./scripts/setup.sh
```

Setup follows this collection’s adopted pins, not upstream’s latest development branches. Rerunning it at the current pins needs no fetch. `--check` only reports drift; running setup repairs clean revision mismatches. If you edit a source under `repos/`, commit, stash, or move those edits before updating.

Start a new chat after installation so Codex reloads the skill catalog. Invoke skills with `$skill-name`. Only `effect` allows implicit invocation; every other skill requires an explicit request. Workflows read sibling skill instructions when their phases need them. The retained specialists keep their invocation settings.

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
$ask-emil improve this dialog's layout and keyboard interactions.
$effect review this worker's interruption, retries, and resource lifetime.
```

`poteto-mode` coordinates engineering work through its own skills, principles, and playbooks. Use `$ask-emil` to choose an Emil UI or motion skill. Poteto does not invoke Emil skills automatically. The 23 playbooks under `skills/poteto-mode/playbooks/` remain ordinary resources, not extra registered skills. `$effect` directs agents to the installed Effect package’s guidance and source.

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
| `create-formal-verification-skill` | Generate and prove a project-specific formal verification workflow. |
| `maintain-formal-verification-skill` | Keep formal models, properties, and harnesses aligned with changed code. |
| `statechart` | Check TLA+ models and draw statecharts with paths to broken rules. |
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

### Emil

Use `$ask-emil` to choose a specialist, or invoke one directly. These replace the local `design` and `design-*` adapters. Good CSS is removed. The existing installation exclusions (`ask-sonner`, `pick-ui-library`, `write-swift`, `animate-expo`) remain; upstream references to them are preserved. All entries are explicit-only.

| Skill | Purpose |
| --- | --- |
| `animate` | Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, what purpose, which tool, which properties, which curve and duration, how it interrupts, how it exits. Writes the implementation. Use when asked to animate something, add motion, make a component feel alive, or build a transition. For critiquing existing motion use review-animations; for auditing a whole codebase use improve-animations. |
| `animation-performance` | Keep web animations inside the frame budget — animate composite-only properties, keep motion off the main thread when the page is busy, and find the cause when an animation drops frames. Use when an animation is janky, choppy, stutters, or drops frames; when choosing which property to animate; when deciding between CSS and JS animation on performance grounds; or when reaching for `will-change` or GPU layers. For choosing easing, duration, or whether to animate at all use animate; for reviewing motion as a whole use review-animations. |
| `animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). Use when the user asks "what's it called when…", or describes a motion effect without knowing its name and wants the right word to prompt an AI or designer with. For naming an effect, not designing or building one. |
| `apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI, spring animations, drag/swipe/sheet interactions, momentum and interruptible transitions, translucent materials and depth, typography (optical sizing, tracking, leading), reduced-motion, or the design foundations (feedback, spatial consistency, restraint) behind Apple-style interfaces. |
| `ask-emil` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `break-ui` | Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts, zero items, long labels, non-Latin text, emoji, extreme numbers — then render it behind a "Demo data / Worst case" toggle and report everything that broke, with the fix for each. Use when the user asks to stress-test, break, or find edge cases in a component or screen, or to "try the worst case". For visual design critique use emil-design-eng; for motion use review-animations. |
| `choreograph` | Coordinate several elements that animate together — decide what moves, in what order, how much they overlap, and what stays still — so a group reads as one intentional motion instead of a pile of separate animations. Use when building or fixing a staggered list, a hero entrance, a view swap inside a container, a multi-step flow, an element leaving while its siblings close the gap, a morph between rich states, or any interaction with several moving parts (icon + background + lines, panel + content, items flying into a target). Triggers on — stagger, sequence, choreography, "one after another", crossfade, AnimatePresence mode, hero entrance, multi-step, useAnimate, "feels mechanical", "too much going on", "feels slow to open". |
| `emil-design-eng` | Emil Kowalski's design-engineering philosophy for UI polish, component design, animation decisions, and the invisible details that make software feel great. Use when building or reviewing a UI component's interactions and polish (press and hover states, popover origin, tooltip timing, transitions vs keyframes, clip-path techniques, drag details) and no narrower skill fits. |
| `find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion with exact values, it does not implement it. Use when the user asks "what could be animated here?" or wants to "make this feel more alive". For fixing existing animations, use improve-animations or review-animations instead. |
| `gestures` | Build drag, swipe, and sheet interactions that track the finger 1:1 and stay interruptible. Use when building or fixing anything the user drags, swipes, flings, holds, or dismisses with a gesture — drawers, sheets, swipe-to-dismiss toasts and cards, drag-to-reorder, pull-to-refresh, hold-to-confirm — or when a gesture feels laggy, disconnected from the finger, jumps on release, or can't be caught mid-animation. Triggers on — gesture, drag, swipe, fling, sheet, snap points, Vaul, Motion drag props, rubber-band, pull to refresh, hold to delete, touch-action, "doesn't follow my finger", "jumps when I let go", "can't grab it mid-animation". |
| `improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. Read-only on source code — it plans improvements, it does not apply them. Use when the user asks to "improve the animations", "audit the motion", "make this app feel better", or wants a roadmap of animation fixes rather than a review of a single diff. |
| `learn-taste` | Turn a session's design corrections into rules, with their why, in DESIGN.md, a project skill, or a lint check. |
| `mobile-native` | Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something that feels installed. Covers sticky hover states, tap highlight flashes, the 100vh bug, inputs that zoom the page, laggy taps, pull-to-refresh hijacking scroll, content under the notch, long-press selecting button text, carousels that scroll the wrong way, mismatched status bars, and the rule that you test on real hardware. Use when a web app is being built for or reviewed on mobile, when something "works in Chrome but feels wrong on my phone", when building a PWA, a bottom sheet, a carousel, a full-screen layout, or any touch interaction. For motion itself use animate; for React Native use animate-expo. |
| `prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live and promote the one that feels right. |
| `remove-animations` | Find the animations an interface doesn't need and remove them — motion on keyboard actions, high-frequency surfaces, functional data, and decoration with no purpose — then clean up what they leave behind. Edits code, but only to subtract; it never adds or retunes motion. Use when the user says the app "feels slow", "has too much animation", "feels over-animated", wants to "tone down the motion", or asks what animations to remove. For finding places that should animate, use find-animation-opportunities; for fixing animations that should stay, use improve-animations or review-animations. |
| `review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned. |

### Cursor Team Kit

| Skill | Purpose |
| --- | --- |
| `deslop` | Remove unnecessary AI-generated code patterns from the branch diff while preserving behavior. |

Copied byte for byte from `cursor-team-kit/skills/deslop/SKILL.md` in the same Cursor plugins revision recorded for Poteto in [UPSTREAM.md](UPSTREAM.md). It supplies the pre-commit cleanup referenced by pstack. Invocation is explicit-only.

### Effect

This local skill is version-independent: it reads the consuming project’s installed Effect guidance and source. Setup requires no Effect reference clone and update checks do not track Effect releases.

| Skill | Purpose |
| --- | --- |
| `effect` | Write and review Effect code using the installed package’s guidance and source. |

### Stageshow

| Skill | Purpose |
| --- | --- |
| `stageshow` | Build polished product UI illustrations, feature cards, bento grids, and animated cursor demos with React and CSS. |

From [Benji Taylor's skills](https://github.com/benjitaylor/skills), installed with its complete kit, examples, references, and filming tools. Invoke `$stageshow` with your illustration or demo brief. Follow its README for optional playground dependencies; setup does not install npm packages.

### Delivery entry points

These personal skills use the existing pstack workflows. Their finish conditions and task permissions are inspired by [tstack](https://github.com/t3dotgg/tstack/tree/1085050f3baed1ac724caa4a8166145fb2ac88af/skills), with no tstack installation or fixed reviewer model. They are maintained locally rather than generated from Poteto.

| Skill | Purpose |
| --- | --- |
| `full-send` | Build, prove, independently review, open a PR, babysit, and merge the requested change. |
| `full-stop` | Perform the same work through merge-ready, leaving the PR open for the user to merge. |

```text
$full-send fix duplicate rows when the importer retries.
$full-stop add keyboard navigation to the picker.
```

Use these skills through an explicit request. Discovery alone does not grant their task-branch, testing, or merge permissions. Full-stop prevents auto-merge and merge-queue entry. Both use Poteto's implementation, verification, review, and PR playbooks; full-send also uses Shipping.

## Source fidelity

Imported Poteto, Emil, Cursor Team Kit, and Stageshow files match their adopted upstream sources byte for byte, including frontmatter and supporting resources. The only local invocation addition is `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. Upstream tool names, model defaults, paths, slash-command examples, and references to excluded skills remain unchanged.

Regenerate Poteto with `scripts/port_poteto.py` and Emil with `scripts/port_emil.py`. Refresh `deslop` from the adopted Cursor plugins checkout with `git -C repos/pstack show HEAD:cursor-team-kit/skills/deslop/SKILL.md > skills/deslop/SKILL.md`. Setup syncs Stageshow's regular `SKILL.md` copy; its resources remain linked. [POTETO.md](POTETO.md) records the import policy; [UPSTREAM.md](UPSTREAM.md) records the pins. Effect, full-send, and full-stop remain locally maintained.

## Validation

```bash
python3 scripts/port_poteto.py --check
python3 scripts/port_emil.py --check
python3 scripts/validate.py
python3 tests/test_validate.py
python3 tests/test_port_poteto.py
python3 tests/test_setup.py
./scripts/setup.sh --check
```

Collection validation checks the included catalog, invocation policy, README coverage, stated catalog counts, local Markdown links and heading anchors, and exact upstream file fidelity. Validator tests exercise documentation failures in temporary fixtures. Installer tests use temporary directories and local Git fixtures, with no changes to global skills and no network fetching.

The imported GitHub watcher and plan-checking helpers require Bun. When changing those helpers, run from `skills/poteto-mode/scripts`:

```bash
bun install --frozen-lockfile
bun test watch-pr check-plan.test.ts
bun run typecheck
```

Without Bun, skills use their documented direct-tool fallback. The helpers are not required for skill installation or discovery.

The statechart compiler uses a TypeScript-capable runtime through `skills/statechart/scripts/statechart`. Run its checks from `skills/statechart/scripts`:

```bash
npm install --no-package-lock
npm test
```

Live TLC checks require Java and `TLA2TOOLS` pointing to `tla2tools.jar`; without it, those tests report skips.
On macOS, use `TMPDIR=/private/tmp npm test` if the default temporary directory contains a symlink; upstream's relative-symlink fixture assumes a canonical path.
