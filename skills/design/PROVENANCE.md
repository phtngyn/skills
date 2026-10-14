# Source and ownership

`SKILL.md` is our personal Codex entry point and routing wrapper. The Emil design guidance comes directly from [Emil Kowalski's skills](/Users/phtngyn/Developer/skills/repos/emil), unchanged in `repos/emil`. CSS implementation uses Vojta Holik's [Good CSS](/Users/phtngyn/Developer/skills/repos/good-css), unchanged in `repos/good-css`, through the internal [CSS reference](references/GOOD_CSS.md). Its MIT license is retained in [GOOD_CSS_LICENSE](licenses/GOOD_CSS_LICENSE). The personal [integration rules](references/CSS_INTEGRATION.md) preserve project constraints and resolve overlapping motion and mobile advice. Good CSS has no separate skill entry point.

Source links use absolute paths to the [cloned Emil skills](/Users/phtngyn/Developer/skills/repos/emil/skills). No upstream directory link is nested under the installed wrapper, preventing independent discovery of excluded skills through it. The upstream checkout and its resources are runtime dependencies; no rewritten supporting guides are bundled here. The retained upstream MIT license identifies the source's terms. This wrapper does not imply Emil authored or endorsed our customizations.

The wrapper adds only routing, personal collaboration preferences, Codex tool adaptation, and maintenance instructions. The commit in the collection's `UPSTREAM.md` identifies the upstream version used. Keep the checkout at that commit until an update is deliberately adopted.

The wrapper excludes `ask-sonner`, `pick-ui-library`, `write-swift`, and `animate-expo` by user preference. They remain unchanged in the upstream checkout for source integrity but are not routed to or loaded by this mode.
