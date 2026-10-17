---
name: no-comments
description: "Review comments, remove accepted clutter, and propose enforceable forms for claimed constraints. Use for $no-comments or a focused comment review."
---

# No comments

Review comments in the caller's files or diff. Without an explicit scope, use the current diff against its actual base, including working-tree changes.

Read [the reviewer contract](references/comment-reviewer.md). Launch a fresh read-only reviewer through the [Codex delegation contract](../poteto-mode/references/codex.md), passing that contract and the exact scope. This replaces the upstream specialized reviewer dependency. If delegation is unavailable, do the review directly and disclose the missing independent pass.

Inspect every finding against source. Reject scope escapes, incorrect claims, and deletions of proven external constraints. For ambiguous warnings, use `how` or `why` to establish the underlying reason before editing.

Apply accepted comment removals and the smallest in-scope root-cause fixes. For a structural fix, run `architect` at sketch scope before implementing. Never hide a defect by deleting the explanation or adding a symptom guard.

For constraints expressible as types, tests, lint, or runtime checks, show a concrete enforcement proposal. Apply it when authorized by the existing task; otherwise leave the constraint intact and report the proposal. Preserve public API documentation, licenses, required directives, and explanations of constraints outside this code's control.

Report accepted removals, code fixes, retained constraints, and unresolved findings. Re-run affected checks after fixes.
