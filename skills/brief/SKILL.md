---
name: brief
description: Turn rough ideas or conversations into concise execution prompts when the user wants help preparing a task or handoff for an agent.
---

# Brief

Turn the supplied idea or conversation into a task an agent can execute. The user sets the outcome and constraints; the executing agent chooses implementation details within that authority.

## Establish the task

Use the supplied idea, notes, or discussion. For a bare invocation, use the current task when clear; otherwise ask what the user wants to accomplish. Preserve the requested kind of work: explanation, exploration, review, planning, or implementation.

Inspect relevant project instructions, files, decisions, and connected sources using read-only operations. Find facts that affect scope, constraints, or verification yourself. Keep discovery proportional to the brief and record unavailable context as a gap; paths, commands, behavior, and measurements need evidence.

Identify the desired change, who benefits, what must remain true, and what evidence would establish success. A clear small request can go straight to a brief.

## Clarify intent

Ask only questions whose answers materially change the outcome, scope, constraints, or decision authority. Resolve technical facts through inspection; leave ordinary implementation choices to the executing agent.

Use small rounds, usually one to three concise questions, with a recommendation and a plain-language tradeoff. Settle prerequisites before dependent questions and reuse accepted decisions from the conversation.

When the user is unsure, explain the options and recommend a path. Record decision authority only when the user grants it; unanswered recommendations remain proposals. Honor requests to draft immediately using stated assumptions.

Finish clarifying when the agent knows what work it may start and how to recognize completion. Technical unknowns can become investigation work. Keep unresolved intent or authority explicit; when it blocks execution, label the brief a draft and name the missing decision.

## Compose the execution prompt

Return one copyable Markdown prompt that stands alone. Keep it as short as the task permits; use these sections where helpful and omit empty ones:

- **Outcome:** The desired behavior or deliverable and why it matters.
- **Context:** Verified facts, accessible source pointers, and the project location when needed. Reference existing specs, decisions, and artifacts; state access gaps.
- **Scope and constraints:** The full requested work, compatibility requirements, and agreed exclusions. Separate proposed scope changes from accepted requirements.
- **Acceptance and verification:** Observable conditions for success and the checks or artifacts that can establish them. For a bug, include known reproduction steps; for a review, define the findings expected. Mark proposed criteria as proposals. Tie targets and commands to supplied requirements or inspected sources.
- **Decision authority:** Choices the agent may resolve and consequential choices to bring back with a recommendation. Preserve existing authorization and mark additional permissions as proposals. Bound implementation freedom by the agreed outcome and constraints.
- **Assumptions and open decisions:** Separate assumptions from confirmed requirements and verified facts. Distinguish blocking decisions from facts to investigate.
- **Handoff:** The result, concrete verification evidence, material limitations, and decisions the user needs to make. Suggest relevant skills only when they fit the task; identify unverified availability rather than implying a skill is installed.

Keep technical detail that encodes a real contract or accepted decision. Let the executing agent choose methods where the user has delegated them. Reuse the user's domain terminology.

## Check and hand off

Check that the prompt preserves scope and request type, defines success, and keeps proposals and unknowns visible. The executing agent should be able to locate context and recognize its decision boundaries without this conversation.

Present a short summary followed by the prompt. For a draft, also identify blocking decisions outside the prompt. Save a file when requested or required by the established task workflow; otherwise return the brief in the response.

Preparation alone does not authorize implementation, creating another chat, publishing a ticket, or sending the handoff. Stop at the brief unless the task already authorizes execution or transmission; then continue within that authorization.

This entry point is self-contained. [Provenance](PROVENANCE.md) records the authoring sources and personal choices.
