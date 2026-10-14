# Source and ownership

`SKILL.md` is our personal Codex authoring wrapper around [Matt Pocock's Writing for Agents](/Users/phtngyn/Developer/skills/repos/mattpocock/skills/productivity/writing-for-agents), reviewed at `f3fc5632f401156837ee3872f14fe33ccf1024ea`. Its original `SKILL.md` and conditional `SKILL-MECHANICS.md` remain unchanged in `repos/mattpocock/skills/productivity/writing-for-agents`.

The wrapper adds the user's preference for documents grounded in authoritative sources: distinguish current behavior from requirements, verify the supporting source before citing it, favor pointers over duplicated facts, and identify version context and useful refresh triggers for volatile claims. These additions extend upstream's single-source-of-truth and environment-as-authority guidance. They are our personal choices, not statements authored or endorsed by Matt.

The skill is an independent entry point, separate from `build`. It retains normal automatic selection for agent-facing documentation and adapts skill packaging to Codex's available `skill-creator` guidance.

The local upstream checkout and its resources are runtime dependencies outside the installed wrapper. Source links use absolute paths into that checkout. The retained upstream MIT license identifies the source's terms. [UPSTREAM.md](../../UPSTREAM.md) records the shared Matt pin and maintenance policy; source bodies are not copied into this wrapper.
