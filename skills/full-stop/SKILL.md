---
name: full-stop
description: Carry a task through a verified, reviewed, merge-ready PR using pstack, leaving the merge to the user. Use for full-stop, full stop, or fullstop requests.
---

# Full stop

Read [full-send](../full-send/SKILL.md) and follow its pstack execution, proof, independent review, PR creation, and babysitting workflow with the overrides below. An explicit full-stop request grants its task-branch update and testing permissions, but never its merge permission. These overrides take precedence over full-send and all inherited playbooks. Automatic discovery alone grants no permission.

## Never merge

Do not merge, enable auto-merge, enter a merge queue, push to the default branch, bypass protection, or delegate those actions. This restriction applies to every owner and reviewer brief.

Before work begins, find any existing PR for the task branch. If one exists, disable auto-merge and remove it from any merge queue. Repeat the check before each push and at handoff. Report any settings changed. If automatic merging cannot be prevented, stop and report that blocker.

For a queue, use [Autopilot-stack](../poteto-mode/playbooks/autopilot-stack.md), with this skill's no-merge rule in every brief. For a single task, follow the matching implementation playbook through babysitting. Run only Shipping's independent verifier procedure and verdict checks, as routed by full-send. Never execute its merge steps or an inherited Autopilot-full merge step.

## Handoff

Apply full-send's merge gate as a readiness gate without merging. Fetch the target and inspect the live PR's head, base, checks, reviews, mergeability, draft status, and automatic merge settings. Proof and independent verification must cover the final change, including meaningful conflict fixes.

Unwatch before handing back. Report one of:

- **Ready to merge.** The gate passes. The PR is open, not a draft, and cannot merge automatically.
- **Waiting for required approval.** Human approval is the only remaining gate. Name the missing approval.
- **Blocked.** State the failed gate, what was tried, and what is needed. Follow full-send's question rules when user input is required.

If another actor merged or closed the PR, report its actual state rather than claiming it remains ready.

Include each PR link, proof, review outcome, and decisions made for the user. Leave the final merge to the user.
