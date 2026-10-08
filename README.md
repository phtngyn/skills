# Personal skills

A Codex-only collection of personal workflows and entry points backed by tracked upstream sources.

Each skill is available through a matching symlink from `~/.agents/skills/<name>` to this collection's `skills/<name>` directory. Keep the collection layout and local upstream checkouts available. Start a new chat if the skill picker has not refreshed.

## Emil

Use `/emil <prompt>` through Codex's skill picker, or explicitly name `$emil` in a prompt. The entry point owns design exploration, UI implementation, motion, critique, mobile polish, and UI stress checks. Upstream skills and their references load only when relevant.

Examples:

```text
/emil this settings screen feels crowded. Recommend a direction before changing it.
/emil explore three different versions of this pricing card.
/emil implement the selected version and verify its interactions.
/emil make this drawer feel responsive without adding unnecessary motion.
/emil review this component with long labels, empty data, and a narrow viewport.
```

The wrapper lives in `skills/emil`. It routes directly to Emil's unchanged upstream skills through direct file references to `repos/emil/skills` outside the installed wrapper. Keep that checkout available at the commit recorded in [UPSTREAM.md](UPSTREAM.md). There are no rewritten supporting guides.

Follow-ups continue the design task without setting an application-wide mode.

## Good CSS

Use `/good-css <prompt>` or explicitly name `$good-css` for CSS implementation and review. It is also available for automatic selection on CSS tasks. The wrapper reads Vojta Holik's unchanged upstream entry point and only the technique entries relevant to the work.

Emil supplies visual direction, component craft, animation decisions, and mobile interaction guidance. Good CSS supplies layout, sizing, typography, overflow, and native CSS techniques. The Emil wrapper reaches it during CSS implementation or review; the [Good CSS wrapper](skills/good-css/SKILL.md#combine-with-emil) resolves overlaps while preserving project tokens, browser targets, and required behavior.

```text
/emil polish this settings page using the existing design system and modern CSS.
/good-css simplify this card grid without changing its behavior.
/good-css check this dialog's CSS against our supported browsers.
```

The entry point lives in `skills/good-css` and reads the pinned `repos/good-css` checkout. Use [good-css.com](https://good-css.com/) for live specimens when a technique needs visual or interaction context. The source references remain the adopted baseline; the live site can differ.

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

The wrapper lives in `skills/build`; its direct upstream references depend on the pinned local clones outside the installed skill directory. Visual design work routes to the personal Emil entry point.

## Effect

Use `/effect <prompt>` or explicitly name `$effect` for Effect applications and reusable libraries. Applications are the default. The skill covers design principles, naming, structure, style, and focused topic guidance while using compatible local source to establish API facts.

The agent locates `repos/effect` in the project or a nearby ancestor, with this collection's clone as a fallback. It compares the checkout with the consuming package, looks up each material changed API/pattern once, and reuses that evidence during the task. Exact signatures, exports, and operational semantics remain source lookups.

```text
/effect design this service and its resource lifetime before implementing it.
/effect review this worker's cancellation, retries, and layer sharing.
/effect design a reusable module and verify its consumer inference.
```

The entry point lives in `skills/effect`. `build` can guide the overall task while Effect supplies language and library decisions. [Provenance](skills/effect/PROVENANCE.md) distinguishes upstream evidence, synthesized principles, and personal preferences.

## Upstream maintenance

For cloning sources, fetching updates, and adopting revisions, follow [UPSTREAM.md](UPSTREAM.md).
