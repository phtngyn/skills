---
name: ketchup
description: "Catch the user up on changes in this chat and list every pending decision with enough context to decide from the reply. Use for $ketchup."
---

# Ketchup

Catch the user up on what changed since their last message before `$ketchup`, and help them understand what each change means. Notifications and subagent results are not user messages. Assume the user remembers their last message and nothing after it.

Use [`$bro`](../bro/SKILL.md)'s voice: plain words, short sentences, and concrete outcomes. Say what changed for the user. Include technical identifiers, commands and counts only when they help the user assess the result or act.

## Gather what changed

Keep this turn read-only apart from creating presentation artifacts from existing evidence. Do not change code, start an app or job, or post anything to prepare the report. When an execution workflow calls this skill for an update, this boundary applies to the reporting step; continue the underlying authorized work afterward. Collect work and reports since that message and check the current state of the PRs, checks and agents this chat touched. Verify numbers against their evidence. Missing access remains an explicit gap.

An action item is a decision or step only the user can take, including one still pending from before their last message. Collect every such item. For each, establish what changes for the user, the evidence behind your recommendation, and the risk. Mark a needed fact as unknown when it cannot be checked. Work you can complete yourself is remaining work, not a request for approval. Do not invent a decision or an extra task to fill the reply.

## Write the reply

Open by saying whether anything needs the user. If nothing changed and nothing is pending, say so and stop.

Show existing screenshots or videos inline when they explain a visible change. Use a diagram for relationships, behavior or a before-and-after that prose would explain less clearly. Then give a short outcome and status for each requested item: done, running, failed or unverified. Name bugs found and fixed on the way. Keep the account of what happened brief and spend words on decisions. Never omit an item or remove context needed to decide it to meet a word count. Let the reply grow with the number of pending items. Avoid repeating facts across prose and visuals.

List action items as plain bullets. Give each item's name or identifier, available link, user-visible change, recommendation, supporting evidence, and risk, even when the risk is low. When one decision covers several items, state the shared decision and recommendation once, then list every item separately with its own context and any different recommendation. A count or link to a list does not replace those items; the reply itself must be enough to decide. Explain the cost of waiting when it is more than a delay. Silence is not approval. State remaining work you can do yourself separately. Work still awaiting a required decision is not complete.

For a choice that benefits from visual comparison, reuse the screenshots already shown or compare the options side by side. Explain each option's gain and cost without repeating the comparison elsewhere. Do not force a diagram for a simple status update or approval request.

## Visual evidence

Use the host's available rendering tools and supported formats. A visual should explain a relationship, change or choice; decorative status boxes add little. Follow host instructions for publishing artifacts.

Use screenshots and videos that actually exist. If a visible change has no capture, say so and describe what changed without inventing a screen. Build diagrams and charts only from established facts, and link only artifacts that exist. Catch-up reporting does not itself authorize launching a browser or capturing new app evidence.
