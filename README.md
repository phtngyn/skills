# Personal skills

A Codex-only collection of personal workflows and entry points backed by tracked upstream sources.

Each skill is available through a matching symlink from `~/.agents/skills/<name>` to this collection's `skills/<name>` directory. Keep the collection layout and local upstream checkouts available. Start a new chat if the skill picker has not refreshed.

## Global setup

Clone this repository to a permanent location, then run:

```bash
./scripts/setup.sh
./scripts/setup.sh --check
```

Setup requires Bash and Git, plus network access when upstream clones are missing. It clones missing sources at the adopted revisions in [UPSTREAM.md](UPSTREAM.md), including Effect, and links each top-level skill into `~/.agents/skills`. Rerunning preserves existing links. Existing sources must be clean and match their adopted pins; setup never fetches, advances, or resets them. Use the separate upstream maintenance workflow to adopt updates.

Unrelated global skills are preserved. A conflicting name stops installation before changing links; back up or relocate that entry deliberately, then rerun. Source checkouts and skill resources are verified before links are created. Moving or deleting this collection breaks its installed links.

```bash
./scripts/setup.sh --uninstall
./scripts/setup.sh --target /path/to/isolated-skills
```

Uninstall removes only links pointing to this collection's matching skill directories, including stale links for removed skills. It preserves foreign links, real directories, and upstream sources. `--target` works with all actions. `--check` reports missing sources, revision drift, dirty checkouts, broken resource links, and missing or conflicting installation links without creating directories or fetching.

Run the isolated installer tests with `python3 tests/test_setup.py`; they use temporary directories and local Git fixtures without changing your global skills or fetching from the network.

## Brief

Use `/brief <rough idea>` or explicitly name `$brief` to prepare a task for an executing agent. It inspects relevant context, asks a few questions about intent with recommended answers, and returns a concise, copyable prompt with the outcome, scope, constraints, acceptance criteria, and decision authority. Assumptions and unresolved choices remain visible.

```text
/brief users keep losing edits when they leave this page. Help me define what should change.
/brief turn our discussion into a prompt for an agent to implement.
/brief I want to simplify onboarding, but I am unsure what the first version should include.
```

Brief is an optional preparation step before Build or Design. It stops at the prompt unless execution or transmission is also requested. The self-contained entry point lives in `skills/brief`; [provenance](skills/brief/PROVENANCE.md) records its sources and personal adaptations.

## Design

Use `/design <prompt>` or explicitly name `$design`. Design combines Emil's UI craft, exploration, motion, critique, and mobile guidance with Good CSS's layout, typography, sizing, overflow, and native controls. It loads only matching upstream guidance. Good CSS is an internal reference, with no separate skill command.

```text
/design explore three different versions of this pricing card.
/design implement the selected version and verify its interactions.
/design simplify this card grid using our existing tokens.
/design check this dialog against our browser targets and keyboard requirements.
```

The wrapper lives in `skills/design`, with unchanged pinned sources in `repos/emil` and `repos/good-css`. [CSS integration](skills/design/references/CSS_INTEGRATION.md) resolves overlaps. Use [good-css.com](https://good-css.com/) for live specimens when needed; the pinned source remains the adopted baseline. Follow-ups continue the design task.

## Build

Use `/build <prompt>` or explicitly name `$build`. Poteto supplies the primary implementation, debugging, architecture, refactoring, and review workflows. Matt provides targeted testing, interface, and diagnostic guidance, with planning and review workflows available on request. Specs and tickets are opt-in.

Start from the code, choose a lightweight foundation, build the simplest complete solution, and verify it. Every implementation ends with a required cleanup and simplification pass; recheck behavior after cleanup changes. Backward compatibility is opt-in: migrate callers to the best current design and remove obsolete APIs and compatibility layers.

The entry point indexes all 24 Poteto principles and reads their original files when task conditions match. You can also name a principle directly to steer a decision.

```text
/build help me settle the behavior of this import flow before implementing it.
/build implement the agreed retry behavior and verify it.
/build diagnose why this job sometimes runs twice.
/build refactor this module while preserving its behavior.
/build apply subtract before you add to this refactor.
/build review these changes against the task and project conventions.
```

The wrapper lives in `skills/build` and adapts the pinned local upstream guidance to Codex. Its source checkouts remain outside the installed skill directory. Visual design work routes to the personal Design entry point.

## Effect

Use `/effect <prompt>` or explicitly name `$effect` to design, implement, refactor, or review Effect v4 applications and reusable libraries. Applications are the default. The skill starts from domain capabilities, failure contracts, and ownership, then routes to focused architecture, boundary, lifetime, concurrency, operations, and testing guidance.

The agent uses project code and focused source lookup to settle unfamiliar APIs or uncertain semantics. Effect's local examples and declarations supply library evidence; the OpenCode v2 study supplies application examples.

```text
/effect design this service and its resource lifetime before implementing it.
/effect review this worker's cancellation, retries, and layer sharing.
/effect design a reusable module and verify its consumer inference.
```

The entry point lives in `skills/effect`. `build` can guide the overall task while Effect supplies language and library decisions. [Provenance](skills/effect/PROVENANCE.md) distinguishes upstream evidence, synthesized principles, and personal preferences.

## Write

Use `/write <prompt>` or explicitly name `$write` to write or review documents agents consume. It is also available for automatic selection on agent-facing documentation tasks. This is a separate writing entry point backed by Matt Pocock's original guidance; Build keeps its existing scope.

Ground claims in authoritative code, configuration, accepted requirements, or version-matched official documentation. Prefer pointers over duplicated facts, cite the supporting source, and record relevant version context and refresh triggers when volatile facts must be repeated. A citation helps verify a claim; it does not make a copied statement permanently current.

```text
/write improve AGENTS.md using the project's authoritative files while preserving its requirements.
/write write an agent guide to this release flow and cite the code and configuration that define it.
/write review these docs for stale claims, weak source links, and unnecessary duplication.
```

The wrapper lives in `skills/write` and reads the pinned `repos/mattpocock` checkout. Skill-specific mechanics load only when authoring a skill. [Provenance](skills/write/PROVENANCE.md) records the source and our personal additions.

## Personal commands

`/bro` (or `$bro`) restates the last response in plain language. It remains manual-only, with its original instructions copied unchanged from the pinned Poteto checkout. Other personal skills do not invoke it.

`/ketchup` (or `$ketchup`) catches you up on chat progress since your previous message and explains decisions awaiting you. It remains manual-only, with its original instructions copied unchanged from the pinned Poteto checkout. There is no custom workflow; [provenance](skills/ketchup/PROVENANCE.md) records the upstream copy and Codex metadata.

## Upstream maintenance

For cloning sources, fetching updates, and adopting revisions, follow [UPSTREAM.md](UPSTREAM.md).
