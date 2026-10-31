---
name: full-send
description: Carry a task through a verified, reviewed, merged PR using pstack. Use when the user explicitly requests full-send or full send.
---

# Full send

An explicit request for this workflow authorizes completing the named task through merge. Automatic discovery alone grants no permission. If the user requests full-stop or says not to merge, follow [full-stop](../full-stop/SKILL.md) instead.

## Scope and permission

Work autonomously on the requested goal. This request authorizes committing, pushing, rebasing, and force-pushing only this task's branch with `--force-with-lease=<branch>:<observed-remote-sha>`, and merging its PR after the gate below passes. Preserve unrelated work. Create a task branch before changing code on the default branch. Record the remote head before rewriting; if the lease fails or another writer advances it, fetch and reassess instead of overwriting their work.

The request also authorizes the tests needed to prove this task, including running the app, browser or device automation, and screenshots, even when project guidance normally says to ask first or leave testing to the user. Follow the project's testing methods and the harness's tool and approval rules. This grant excludes deployments, production mutations, data deletion, closing PRs, and rewriting unrelated or shared branches.

## Execute with pstack

Read [poteto-mode](../poteto-mode/SKILL.md) and use its matching implementation playbook and configured roles. This skill supplies the end condition and task-specific permissions. Its permission boundaries and finish mode override conflicting playbook defaults. Carry the active mode and this skill's path into every implementation or owner brief. Poteto owns implementation, proof, review, and PR conventions; use its configured reviewers.

For one task, carry its implementation playbook through completion. For a queue, use [Autopilot-full](../poteto-mode/playbooks/autopilot-full.md). Keep a decision trail with [show-me-your-work](../show-me-your-work/SKILL.md).

1. Finish the smallest change that achieves the goal. Reproduce reported failures before fixing them.
2. Prove the final behavior on the real artifact using the project's verification workflow. Run relevant checks and add a focused regression test when warranted. For runtime or UI changes, observe the actual behavior; mocked tests alone are insufficient. Record missing proof as a blocker.
3. Open or update the PR through [Opening a PR](../poteto-mode/playbooks/opening-a-pr.md). Include concise proof. This invocation explicitly requests the subsequent babysit, so continue rather than stopping at PR creation.
4. Obtain independent review and verification under Poteto's rules. For a single PR, use the verifier procedure and verdict rules in [Shipping](../poteto-mode/playbooks/shipping.md) steps 1 and 3; do not perform its merge steps yet. For a queue, use Autopilot's independent swarm. Verify findings, fix real defects, decline scope expansion with evidence, and refresh review or proof when behavior changes. If the required reviewer or tools are unavailable, report the gap rather than inventing approval.
5. Drive [Babysit](../poteto-mode/playbooks/babysit.md) to merge-ready. Fix real CI and review findings and prove each behavioral fix before pushing. When a rebase is needed, act as the task's branch owner outside the babysit pass, then resume it.
6. Apply the gate below, then run [Shipping](../poteto-mode/playbooks/shipping.md). Confirm GitHub reports merged; enabling auto-merge or entering a queue is not completion.

## Merge gate

Check the live head, base, checks, reviews, and mergeability immediately before shipping. Every condition must hold for the code that lands:

- Direct proof covers the final behavior diff, and independent verification covers the current patch under Poteto's verdict rules.
- Required checks pass, the repository's expected review bots have reviewed the current head, and each finding is fixed or dismissed with a written reason. Do not wait for a bot the repository does not use. CodeRabbit is advisory; do not wait for it.
- No human review still requests changes, and required approvals are present.
- The branch is current with its target and mergeable. Fetch before the final check. If behind or conflicted, rebase as the owner, push with the pinned lease, and obtain fresh checks and any invalidated proof or review.

Use the repository's merge method and branch protection. Never bypass protection or use `--admin`. For stacks, preserve Poteto's independent verdicts and bottom-up shipping order.

## Waiting and blockers

Use the host's PR event watcher when available. In T3 Code, handle current findings, call `watch_pull_request`, and end the turn so events resume the work. Only the PR-owning thread watches. Outside T3, use Poteto's watcher. Never run duplicate watchers or a separate polling loop. Unwatch before a final handoff or a question; a watcher continuation is not a completed handoff.

Ask through the harness's question tool only when proof cannot be obtained, a gate cannot be cleared, the goal needs a consequential product decision, or the next action exceeds this grant. Include the PR, evidence, and recommended choice. If no answer is available, leave the PR open and unmerged and report the blocker. Never treat silence, an exhausted review budget, or a tool failure as approval.

Report the PR link, confirmed merge commit, proof, review outcome, decisions made for the user, and any remaining limitations. Never claim completion while the PR is merely queued or waiting.
