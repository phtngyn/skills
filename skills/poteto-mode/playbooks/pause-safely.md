### Pause safely

1. On an explicit pause or stop, stop launching work and notify active children. Interrupt or drain them through available agent tools. Respect a request for an immediate stop.
2. Preserve uncommitted work, evidence, and logs. Record current branch and revision, completed units, outstanding gates, and the exact next step. Do not commit, push, merge, or delete simply to make a checkpoint unless authorized.
3. Identify processes and watchers started by this run. Stop owned processes that should not outlive it and report any still running. Never kill unrelated processes by name.
4. Return a compact handoff with artifact paths, unresolved blockers, and restart instructions. For imminent compaction, make this checkpoint and continue the authorized task afterward; compaction is not a user pause.
