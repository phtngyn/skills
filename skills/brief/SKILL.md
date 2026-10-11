---
name: brief
description: Turn rough ideas or conversations into concise execution prompts when the user wants help preparing a task or handoff for an agent.
---

# Brief

Prepare a task the user can delegate. The user manages outcomes; the executing agent owns implementation. Accept rough language and use the conversation instead of making the user fill in a template.

## Establish the task

Use the supplied idea, notes, or existing discussion. For a bare invocation, use the current task if it is clear; otherwise ask what the user wants to accomplish. Preserve the requested kind of work: explanation, exploration, review, planning, or implementation.

Inspect relevant project instructions, files, existing decisions, and connected sources within the task's scope using read-only operations. Find project facts yourself. Keep discovery proportional to the brief; investigate only facts that affect its scope, constraints, or verification. If context is unavailable, record the gap rather than inventing paths, commands, current behavior, or measurements.

Identify the desired change, who benefits, what must remain true, and what evidence would establish success. A clear small request can go straight to a brief.

## Clarify intent

Ask only questions whose answers materially change the outcome, scope, constraints, or decision authority. Resolve technical facts through inspection; leave ordinary implementation choices to the executing agent.

Use small rounds, usually one to three concise questions. Offer a recommendation and explain the tradeoff in plain language. Ask dependent questions after their prerequisites are settled. Reuse answers and accepted decisions already in the conversation.

If the user says they do not know, explain the practical options and recommend a path. Record a choice as delegated only when the user delegates it. An unanswered recommendation remains a proposal. Honor requests to draft immediately using stated assumptions.

Finish clarifying when the agent can start bounded work and identify the evidence needed for completion. Technical unknowns can become investigation work. Unresolved choices about intent or authority remain explicit; when they block execution, label the brief a draft and name the missing decision.

## Compose the execution prompt

Return one copyable Markdown prompt that makes sense to an agent without this conversation. Keep it as short as the task permits. Use the following sections where they help; omit empty sections and scale detail to the work:

- **Outcome:** The desired behavior or deliverable and why it matters.
- **Context:** Relevant verified facts and accessible source pointers. Include the project location when needed. Reference existing specs, decisions, or artifacts rather than duplicating them. State access gaps.
- **Scope and constraints:** The full requested work, compatibility requirements, and agreed exclusions. Keep proposed scope changes visibly separate from accepted requirements.
- **Acceptance and verification:** Observable conditions for success and the checks or artifacts that can establish them. For a bug, include known reproduction steps; for a review, define the findings expected. Mark proposed criteria as proposals. Tie targets and commands to supplied requirements or inspected sources.
- **Decision authority:** The choices the agent may resolve and the consequential choices to bring back with a recommendation. Carry forward existing authorization accurately; describe additional permissions as proposals. Keep implementation freedom within the agreed outcome and constraints.
- **Assumptions and open decisions:** Separate assumptions from confirmed requirements and discovered facts. Distinguish questions that block execution from facts the agent should investigate.
- **Handoff:** The result, concrete verification evidence, material limitations, and decisions the user needs to make. Suggest relevant skills only when they fit the task; identify unverified availability rather than implying a skill is installed.

Keep technical detail that encodes a real contract or accepted decision. Let the executing agent choose methods where the user has delegated them. Reuse the user's domain terminology.

## Check and hand off

Before returning the prompt, check that it preserves the user's scope and request type, states what success looks like, and keeps proposals and unknowns visible. An executing agent should be able to find the relevant context and recognize its decision boundaries without guessing at missing conversation.

Present a short plain-language summary followed by the copyable prompt. For a draft, identify the blocking decisions outside the prompt as well. Save a file when the user requests one or an established task workflow requires it; otherwise keep the brief in the response.

Stop after preparing the brief unless the user has also requested execution or transmission. Preparing a brief alone does not authorize implementation, creating another chat, publishing a ticket, or sending the handoff. When a broader request already supplies that authorization, finish the brief and continue within it.

This entry point is self-contained. [Provenance](PROVENANCE.md) records the authoring sources and personal choices.
