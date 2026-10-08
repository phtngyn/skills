---
name: build
description: "Explicit software-building entry point. Use /build to implement, debug, refactor, design, or review software with Poteto-led workflows and focused Matt Pocock support."
---

# Build

A personal Codex entry point led by Poteto. Understand the code, choose the data shape, make a coherent change, and prove the result. Matt Pocock supplies focused testing and interface guidance when it answers a concrete question. This wrapper controls routing, effort, collaboration, and authorization, including indirect handoffs to upstream guidance.

## Start and route

For `/build <request>` or `$build`, inspect repository instructions, relevant code, callers, tests, and observable behavior. Code establishes what exists; the user's intent establishes what should change. Existing behavior can be wrong.

A bare invocation asks what to work on. Otherwise begin the actual request. Honor whether the user wants an explanation, a plan, a review, or implementation. Follow-ups continue the task without another invocation; this is not an application-wide persistent mode.

Read the selected upstream file in full before applying it. Resolve its resources relative to its directory and read referenced material when needed. Use one primary workflow per phase. Load supporting guidance for a concrete decision. Use the leaf files below rather than loading Poteto Mode's entire trigger system.

Poteto owns the primary workflows:

| Task | Primary source |
| --- | --- |
| Build or change behavior | [Poteto feature playbook](../../repos/pstack/pstack/skills/poteto-mode/playbooks/feature.md) |
| Fix a reported bug | [Poteto bug-fix playbook](../../repos/pstack/pstack/skills/poteto-mode/playbooks/bug-fix.md) |
| Investigate how existing code works | [Poteto how](../../repos/pstack/pstack/skills/how/SKILL.md) |
| Diagnose measured slowness | [Poteto perf playbook](../../repos/pstack/pstack/skills/poteto-mode/playbooks/perf-issue.md) |
| Choose a consequential architectural shape | [Poteto architect](../../repos/pstack/pstack/skills/architect/SKILL.md) |
| Settle an empirical question with a small experiment | [Poteto prototype playbook](../../repos/pstack/pstack/skills/poteto-mode/playbooks/prototype.md) |
| Review changes against intent and the surrounding code | [Poteto review rubric](../../repos/pstack/pstack/skills/interrogate/references/rubric.md) |
| Refactor while preserving behavior | [Poteto refactoring playbook](../../repos/pstack/pstack/skills/poteto-mode/playbooks/refactoring.md) |

## Principles

Scan this index at the start of a task and when the work changes direction. Select matching principles and any the user names. Read each selected leaf in full before applying it, and load its referenced material only when needed. The personal rules below govern scope, staging, delegation, and external actions.

Use principle names as steering vocabulary. When naming a principle in an explanation, identify the concrete decision it changed. Cite only leaves read during the task.

| When this applies | Principle |
| --- | --- |
| Refactoring, sizing a diff, or considering an abstraction | [Laziness Protocol](../../repos/pstack/pstack/skills/principle-laziness-protocol/SKILL.md) |
| Choosing core types, data structures, foundations, or shared state | [Foundational Thinking](../../repos/pstack/pstack/skills/principle-foundational-thinking/SKILL.md) |
| Integrating a new requirement into an existing design | [Redesign from First Principles](../../repos/pstack/pstack/skills/principle-redesign-from-first-principles/SKILL.md) |
| Two or more fixes sharing one premise fail the same check | [Attack the Premise](../../repos/pstack/pstack/skills/principle-attack-the-premise/SKILL.md) |
| Sequencing an addition, refactor, or rewrite | [Subtract Before You Add](../../repos/pstack/pstack/skills/principle-subtract-before-you-add/SKILL.md) |
| Code is hard to trace through layers or hidden state | [Minimize Reader Load](../../repos/pstack/pstack/skills/principle-minimize-reader-load/SKILL.md) |
| A planned rewrite or migration has explicit phase boundaries | [Outcome-Oriented Execution](../../repos/pstack/pstack/skills/principle-outcome-oriented-execution/SKILL.md) |
| Product, user experience, or feature scope requires a tradeoff | [Experience First](../../repos/pstack/pstack/skills/principle-experience-first/SKILL.md) |
| A novel interaction or architectural choice has no precedent | [Exhaust the Design Space](../../repos/pstack/pstack/skills/principle-exhaust-the-design-space/SKILL.md) |
| Nontrivial implementation, migration, analysis, or verification | [Build the Lever](../../repos/pstack/pstack/skills/principle-build-the-lever/SKILL.md) |
| Stateful logic, repeated branching, or loose data shapes | [Model the Domain](../../repos/pstack/pstack/skills/principle-model-the-domain/SKILL.md) |
| External input, validation, errors, or framework wiring | [Boundary Discipline](../../repos/pstack/pstack/skills/principle-boundary-discipline/SKILL.md) |
| Designing types or function signatures in a typed language | [Type System Discipline](../../repos/pstack/pstack/skills/principle-type-system-discipline/SKILL.md) |
| Commands or lifecycle steps can retry, restart, or resume after failure | [Make Operations Idempotent](../../repos/pstack/pstack/skills/principle-make-operations-idempotent/SKILL.md) |
| Replacing an internal API that still has callers | [Migrate Callers Then Delete Legacy APIs](../../repos/pstack/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) |
| Concurrent actors can write the same file, branch, key, or object | [Separate Before Serializing Shared State](../../repos/pstack/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) |
| Completing work or assessing a claim of success | [Prove It Works](../../repos/pstack/pstack/skills/principle-prove-it-works/SKILL.md) |
| Debugging a symptom or regression | [Fix Root Causes](../../repos/pstack/pstack/skills/principle-fix-root-causes/SKILL.md) |
| Multi-step changes, migrations, or ordered delivery | [Sequence Work into Verifiable Units](../../repos/pstack/pstack/skills/principle-sequence-verifiable-units/SKILL.md) |
| Writing, changing, or retaining a test | [Test Behavior, Not Implementation](../../repos/pstack/pstack/skills/principle-test-behavior-not-implementation/SKILL.md) |
| Trusting, reporting, or acting on a measured number | [Explain the Number](../../repos/pstack/pstack/skills/principle-explain-the-number/SKILL.md) |
| Bulk reading or large outputs are filling the context window | [Guard the Context Window](../../repos/pstack/pstack/skills/principle-guard-the-context-window/SKILL.md) |
| A reversible step can proceed within existing authorization | [Never Block on the Human](../../repos/pstack/pstack/skills/principle-never-block-on-the-human/SKILL.md) |
| The same instruction or correction recurs | [Encode Lessons in Structure](../../repos/pstack/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) |

## Default working loop

1. Trace the affected flow before proposing a redesign. Establish the intended result, current behavior, data shape, ownership, and a check that can distinguish success from failure. For new code, inspect the system it must integrate with.
2. Resolve factual uncertainty by inspecting or running the system. Use a small isolated experiment when observation can settle the choice. Ask about missing intent or consequential product choices with a recommendation. Honor checkpoints the user requests.
3. State the next coherent change and how to verify it. For a consequential architectural choice, sketch caller usage, types, and ownership before implementation. Compare structurally different options when the choice remains uncertain. Ordinary function changes use established patterns.
4. Implement the smallest change that reaches the goal. Prefer structures that remove invalid states, repeated rules, or scattered branching. Preserve the full requested scope. Run the useful check after each meaningful slice and let its evidence determine the next step.
5. Inspect the final artifact and task diff against the request and repository conventions. Complete the verification below before reporting the outcome. Revise the design when evidence refutes it.

The user can begin with a rough goal. Keep planning local to the next verifiable step; useful work can start before a full specification exists. For long work, retain a short record of decisions and remaining work. A request for a plan alone gets a plan grounded in the code.

## Matt supporting guidance

Read a supporting file when its decision arises. It supplements the selected Poteto workflow.

| Decision | Source |
| --- | --- |
| The user requests feature TDD or a test-first implementation | [Matt TDD](../../repos/mattpocock/skills/engineering/tdd/SKILL.md) |
| An interface or testing seam needs a depth and ownership check | [Matt codebase-design](../../repos/mattpocock/skills/engineering/codebase-design/SKILL.md) |
| A stubborn or intermittent bug needs a tighter feedback loop | [Matt diagnosing-bugs](../../repos/mattpocock/skills/engineering/diagnosing-bugs/SKILL.md) |

Feature TDD stays within Poteto's feature workflow. Apply Matt's one-failing-test, one-implementation-slice cadence through caller-facing interfaces. Ask about a new testing boundary only when it changes a consequential contract; established project boundaries and agreed test plans need no repeated approval. Perform structural refactoring after the slice passes, then recheck behavior. Preserve project terminology.

For a requested specification or ticket breakdown, use Matt's [to-spec](../../repos/mattpocock/skills/engineering/to-spec/SKILL.md) or [to-tickets](../../repos/mattpocock/skills/engineering/to-tickets/SKILL.md). Use Matt's [code-review](../../repos/mattpocock/skills/engineering/code-review/SKILL.md) when the user requests that workflow or separate requirements and standards reports. Ordinary reviews use Poteto's rubric. The task brief can supply requirements without a formal specification or tracker setup.

## Verification and review

Use [Prove it works](../../repos/pstack/pstack/skills/principle-prove-it-works/SKILL.md) before declaring implementation complete. Exercise the interaction, API, CLI, or runtime path the user depends on. Compilation and linting establish only their own checks. State missing evidence plainly.

When measuring or reporting a performance change, use the [Benchmark checklist](../../repos/pstack/pstack/skills/benchmark-checklist/SKILL.md) to apply Explain the Number to the actual runs.

For bugs, reproduce the actual symptom before fixing and verify the original scenario afterward. Use [Poteto TDD](../../repos/pstack/pstack/skills/tdd/SKILL.md) when a cheap local regression test exists or the user requests one. When a durable test needs disproportionate setup, use a focused executable check that exercises the failure. Report the failing-before and passing-after evidence, or explain which part could not be established.

For refactoring, pin observable behavior before moving structure and verify it as the structure changes. Migrate callers and remove obsolete code together when safely bounded. A wide rollout may need working intermediate stages; name the contract each stage preserves and remove temporary compatibility at the end.

Capture the starting revision and contents of files with pre-existing changes before editing them. Review staged and unstaged changes plus untracked task files against that starting state, including mixed edits within a file. For committed reviews, use the requested revision comparison. Do not stage or commit merely to make a review visible. Trace actionable findings to reachable behavior and explain their impact. Fix findings within an implementation request; report findings for a review-only request.

## Personal rules and conflict resolution

- Match effort to the task. Architecture exploration is for consequential or uncertain choices, rather than every function boundary. Small changes need a focused implementation and check. Larger work needs verifiable slices. Keep durable records when useful; ordinary work does not require throughput checklists, principle citations, or decision logs.
- Adapt tools to Codex. Upstream references to Skill, Task, Cursor rules, model slugs, or plugins describe intent, not required tool names or dependencies. Read local resources directly. Delegate only when authorized; an upstream demand to delegate does not itself grant permission. Otherwise own the work and perform the checks directly. Inspect any delegated artifact yourself and claim independent review only when it occurred.
- Do not automatically commit, open PRs, publish tickets, merge, deploy, or send messages. Follow task authorization. An implementation request alone does not authorize these upstream closing steps.
- Route visual exploration, UI craft, and motion to the personal [Design entry point](../design/SKILL.md), honoring its exclusions. Keep application behavior, data contracts, and integration verification in this workflow. Use the existing project stack and official version-specific documentation where needed.
- Report the result, consequential choices, concrete verification evidence, and remaining limitations. Give a candid recommendation when a proposed change does not earn its complexity.

## Sources and updates

Source links point outside the installed skill directory into the collection's local upstream clones. Resolve the real path of this wrapper before resolving relative source links. Keep upstream directory symlinks outside the installed wrapper so their skills are not independently discovered through it.

Keep both checkouts at their based-on commits in the collection's [UPSTREAM.md](../../UPSTREAM.md). Fetching must not advance these runtime sources. Adopt updates by reviewing the upstream diff and advancing the clean checkout and based-on record together. If a selected source is missing or at a different revision, report it rather than silently substituting installed skills or changing the pin.

See [provenance](PROVENANCE.md).
