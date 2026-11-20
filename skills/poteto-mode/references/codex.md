# Running Poteto in Codex

## Skills and plans

Use `$skill-name` in chat. From a loaded Poteto skill, read a sibling’s `SKILL.md` by its installed path. Use the current absolute path when passing a skill or helper to a worker. Project skills live in `.agents/skills/<name>/`. Use `skill-creator` for skill authoring when available. Track multi-step work in `update_plan` when exposed, or keep the checklist in the thread.

## Delegation

Read the active host rules first. On T3, use the native Codex `spawn_agent` and `wait_agent` for same-provider work under the inherited settings. Follow the host's instructions for `delegate_task` when a separate checkout, background agent, or a requested setting requires it. Discover capabilities before the first delegate call. Follow the returned continuation and use `task_cancel` to stop a delegated task. Use a supported worktree mode for isolated workers. Where Codex has no isolated agent mode, an ordinary temporary Git worktree is an option only if the host permits it and the worker can actually use it. Check the base and each worker's location before overlapping writes. Give read-only reviewers an explicit read-only brief and separate any repros from the shared tree.

Start each brief with the absolute path to `worker.md`. Include the user's goal, relevant requirements, exact ref or snapshot, write boundaries, and proof. Respect the available concurrency. Wait, cancel, or follow up through the lifecycle tool for the agent you started. If ordinary implementation or exploration can run directly, continue when delegation is unavailable. Report missing independent review or concurrency where it changes the claim.

Models and reasoning inherit by default. Read the applicable role under `roles` in `${CODEX_HOME:-$HOME/.codex}/pstack/roles.json` at the start of a delegated phase when the host permits overrides. Check each saved model and effort against the active tool, including existing entries. Use the inherited setting and record any mismatch when an optional preference is unavailable. For an explicitly requested model, report the blocker rather than substituting. [$setup-pstack](../../setup-pstack/SKILL.md) can change the preferences. Keep experiments and review panels within Codex. Independent seats can use different hypotheses, scopes, or supported Codex models. Report the actual configurations and use serial comparisons with separate outputs when parallelism is unavailable.

## Live app evidence

Use project verification skills, harnesses, and supported app tools, following session and repository browser and device rules. On T3, use `preview_status` and then `preview_open` as needed for requested browser work. Use `device_list` and `device_open` for supported simulators and emulators, then operate the app with the device tool's returned command. Use the project's real CLI, PTY, HTTP harness, or profiler when that matches the surface. Capture the action, the resulting state, and relevant side effects. State the exact missing capability if the live path cannot run. A source read or mock alone cannot prove live behavior.

## Pull requests and unattended work

Use authorized PR and CI tools. On T3, use the available `pull_request_*` tools for reads, lists, creation, edits, reviews, replies, closes, and merges. Use `ci_logs` and `ci_rerun` for checks. Use the forge CLI or bundled GitHub watcher only when the corresponding host tools are unavailable.

Call `link_pull_request` or `link_pull_requests` immediately after taking over or pushing to each affected PR, or after creating a PR outside the self-linking `pull_request_create` tool. Use `watch_pull_request` for an authorized wait, then hand back the turn so a PR event can resume it. Only the owning thread watches. Use `unwatch_pull_request` before final handoff.

Where no host watcher governs the wait and no host tool supplies the operation, use the bundled GitHub watcher at `scripts/watch-pr/watch-pr` under Poteto mode. Without Bun or a usable watcher, take bounded snapshots with the available GitHub connector or forge CLI. Confirm the live PR state and head before reporting a merge.

Keep a defined finish condition and persist in the current run where possible. Schedule a future run only when requested and the host supports it. Use the host's task lifecycle controls for delegated work.

## History and records

Use the current conversation and the host's scoped thread/history tools. On T3, read an identified thread with `t3_thread_read` and cite the thread link returned by the host. Use a user-supplied export when available. Read only in-scope threads and relevant excerpts. If history or tool traces are unavailable, use Git, issue records, and artifacts, and label the evidence gap. Keep private transcript material out of published artifacts.
