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

Use `/build <prompt>` or explicitly name `$build`. Poteto owns the primary implementation, debugging, architecture, refactoring, and review workflows. Start from the code, choose the data shape, implement a coherent change, and verify the actual result. Matt supplies targeted testing, interface, and diagnostic guidance; his planning and review workflows are available when requested. Specs and tickets are opt-in. The wrapper loads relevant upstream guidance and adapts it to Codex.

The entry point indexes all 24 Poteto principles and reads their original files when task conditions match. You can also name a principle directly to steer a decision.

```text
/build help me settle the behavior of this import flow before implementing it.
/build implement the agreed retry behavior and verify it.
/build diagnose why this job sometimes runs twice.
/build refactor this module while preserving its behavior.
/build apply subtract before you add to this refactor.
/build review these changes against the task and project conventions.
```

The wrapper lives in `skills/build`; its direct upstream references depend on the pinned local clones outside the installed skill directory. Visual design work routes to the personal Design entry point.

## Effect

Use `/effect <prompt>` or explicitly name `$effect` for Effect applications and reusable libraries. Applications are the default. The skill covers design principles, naming, structure, style, and focused topic guidance while using compatible local source to establish API facts.

The agent locates `repos/effect` in the project or a nearby ancestor, with this collection's clone as a fallback. It compares the checkout with the consuming package, looks up each material changed API/pattern once, and reuses that evidence during the task. Exact signatures, exports, and operational semantics remain source lookups.

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

`/bro` (or `$bro`) restates the last response in plain language. It remains manual-only, with its original skill linked directly from the pinned Poteto checkout. Other personal skills do not invoke it.

Show Me Your Work is a shared support skill, available automatically for substantial work that needs a decision trail and separate review. Agents select it from its own description; other skills need no routing instructions. Routine edits and simple fixes skip it. You can still invoke `/show-me-your-work` or `$show-me-your-work` explicitly. Start it before a long task to capture decisions as they happen.

Its [local entry point](skills/show-me-your-work/SKILL.md) loads the unchanged Poteto workflow and adds selective activation plus a separate subagent review. When transcripts or another model family are unavailable, it reviews the available evidence and discloses the limits. See [host requirements](skills/show-me-your-work/PROVENANCE.md#host-requirements). Bundled scripts and references remain linked to the adopted checkout; fetching alone preserves that revision.

## Upstream maintenance

For cloning sources, fetching updates, and adopting revisions, follow [UPSTREAM.md](UPSTREAM.md).
