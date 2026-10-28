# Design workflow

Read this for implementation, exploration, or substantial planning. Lookups and read-only critiques use their specialist's method without this implementation workflow. Continue the current phase; do not restart when another specialist is loaded.

## Ground the change

Identify the requested deliverable, the user's task, and the observable result. Inspect the affected source, screen or supplied reference, components, tokens, dependencies, and available checks. Resolve project facts by inspection. Bring consequential product uncertainty to the user with a recommendation.

Before changing ownership, dependencies, or workflow structure, state the intended relationship in one sentence and check it against the user's explicit constraints. Similar organization does not imply a runtime dependency. Put those same constraints in any review or evaluation brief. Proceed when the requirement is clear; this check does not require a new approval.

Preserve the full scope and existing product decisions. Agree on staging for a multi-component exploration rather than silently dropping parts. Track phases for substantial work; keep a narrow fix proportionate to its scope.

## Shape and build

Reuse project components, tokens, and conventions. Name states, events, data, and ownership before stateful UI logic, including relevant loading, empty, error, disabled, and interrupted states. Prefer a clear model to scattered flags. Choose the simplest complete interaction; remove obsolete paths when replacing them.

Use `design-prototype` when alternatives are requested. Make realistic, working variants in an isolated surface and stop for selection before promotion. An agreed direction does not need another variant exercise. Use the smallest isolated experiment to settle an unresolved behavioral question.

Follow the selected construction specialist. Reproduce defects on the matching surface and fix their cause. Preserve semantics, focus, keyboard, touch, and reduced-motion behavior relevant to the change. Planning ends with the requested plan; it does not authorize implementation or unsolicited plan files.

## Verify and deliver

Inspect the rendered result and drive the changed interaction with available control tools. Check relevant viewport sizes, difficult content, and state transitions. Motion needs interruption, rapid retriggering, and exit checks; phone-specific claims need suitable device evidence. Report unavailable checks as unverified.

Run project checks appropriate to the change and test observable behavior when needed. A screenshot establishes appearance, not interaction, and compilation establishes neither. Review the diff for scope, unnecessary layers, dead code, and unsupported claims. Use a fresh read-only reviewer for nontrivial work when supported and authorized, following [delegation](DELEGATION.md).

Report the user-visible result, consequential choice and reason, actual verification, and remaining decisions or checks. Keep prose concrete and comments focused on non-obvious reasons or public contracts. Commits, PRs, publishing, and messages remain governed by task authorization.
