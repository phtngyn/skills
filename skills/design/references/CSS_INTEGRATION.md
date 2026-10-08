# Design and CSS

This is personal integration guidance. Apply it when the selected CSS technique overlaps with motion or mobile interaction advice; read the original entries and the matching Emil branch before choosing.

| Decision | Guidance |
| --- | --- |
| Visual direction, hierarchy, component craft, and design critique | Emil and the project's design system |
| Layout, sizing, typography, color derivation, overflow, and native CSS mechanisms | Good CSS within the project's constraints |
| Whether to animate, timing, springs, interruption, gestures, and mobile behavior | The relevant Emil component or mobile guidance |

Use the [personal Design wrapper](../SKILL.md) to select its upstream branch. Continue the current workflow and reuse material already read.

## Motion recipes

Preserve existing motion tokens and Emil's component-specific choices. A CSS recipe supplies a mechanism; it does not authorize adding motion. Keyboard actions and reduced-motion behavior still follow the selected Emil guidance. Native entry/exit CSS can implement a chosen transition when its behavior fits the target browsers; an existing component's interaction contract remains binding.

The Good CSS [motion category](../../../repos/good-css/skills/good-css/references/motion.md) includes two notable overlaps with Emil's `animate` guidance:

- **Inherited `@property` progress:** the example animates a parent variable used by child transforms. Emil advises applying frequently updated child transforms directly to their owning elements. Use that motion-path guidance rather than automatically adopting the shared parent-variable recipe.
- **Active-item indicator:** the example transitions logical position and size. Emil's animation guidance prefers transform/opacity paths for general UI motion. Separate the useful native positioning mechanism from whether and how its position should animate; follow the relevant component guidance and measure performance claims when they determine the choice.

## Root scrolling

Good CSS's [scroll and viewport category](../../../repos/good-css/skills/good-css/references/scroll-and-viewport.md) restores root bounce on coarse-pointer devices. Emil's `mobile-native` guidance suppresses it for applications that own their scroll containers or gestures while allowing ordinary document behavior.

Choose from the actual page contract: document scrolling and navigation, app-owned scroll areas, pull-to-refresh, and gesture ownership. Apply the relevant mobile branch, then keep inner scrollers and browser navigation usable. Neither source's root rule belongs in every page reset.
