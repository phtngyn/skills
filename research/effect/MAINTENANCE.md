# Effect Skill Maintenance

This directory is maintainer research, outside `skills/effect` and its installed reading paths. It preserves source studies, personal preferences and earlier validation results without making them instructions for ordinary Effect work.

## Current Baseline

On 2026-10-29, npm's `latest` release is Effect 4.1.0. The official `effect@4.1.0` tag resolves to `9a91b1926a5fbfaffd302a7a41a94d4d53a1154e`, adopted in [UPSTREAM.md](../../UPSTREAM.md) with the clean reference checkout at that revision.

The skill uses the consuming project's `repo/effect` clone (or `repos/effect` layout) for release-matched source, focused tests and companion packages. Keep API detail there rather than copying the upstream manual into installed guidance. The release review covers 4.0.7 and 4.1.0; unstable and experimental API annotations matter even when the package release is stable.

Focused installed guidance now covers explicit crypto provision and mocks, opt-in HTTP Problem Details, scoped semaphore permits, cleanup-failure reporting, and migration checks for persisted and wire formats. The mixed-cause and closed-scope fork statements were revalidated on the published 4.1.0 package.

Migration evidence from the [release changelog](https://github.com/Effect-TS/effect/blob/effect%404.1.0/packages/effect/CHANGELOG.md): KVS persistence keys change from concatenated store/key names to separated names, so earlier entries, including persisted chat histories, are unreachable without migration. Redis persistence keys change for store IDs containing `%` or `:`. Redis PersistedQueue locks are incompatible with old workers; stop them and let locks expire before starting upgraded workers on the same prefix. RPC SchemaBinary peers require coordinated upgrades for the changed discard envelope. These are release-specific migration facts, not instructions for every application.

In `/tmp/effect-41-validation.dyyaLh`, all four embedded TypeScript examples and the focused probes compiled with strict TypeScript 6.0.3 against published `effect`, `@effect/vitest` and `@effect/platform-node` 4.1.0. Vitest 5.0.4 passed eight checks: the embedded virtual-time test, mixed-cause recovery and retry, closed-scope immediate and uninterruptible forks, scoped listener disposal, schema decoding, service replacement and error identity, permit release after interruption, and real/mock digest provision. This is focused validation, not a full upstream suite or independent skill-effectiveness evaluation.

## Previous Baseline: 4.0.6

On 2026-10-23, the npm registry's `latest` release was Effect 4.0.6. Its official `effect@4.0.6` tag resolves to `3b28bf686bf26e9700edd39c025aff2744dc5303`, adopted for that revision. Default-branch fetching remains separate from release adoption.

Reviewed the release changelog and guidance affected by mixed causes, closed-scope forks, runtime disposal, callback stream registration, and SQL changes. The failure and concurrency guides now state the relevant 4.0.6 semantics. The existing release-sensitive advice for disposal, stream ownership, and post-commit work remains applicable.

In an isolated temporary npm workspace, all four embedded TypeScript examples compiled with strict TypeScript 6.0.3 against published `effect@4.0.6` and `@effect/vitest@4.0.6`. The embedded virtual-time test passed with Vitest 5.0.4. Three additional published-package checks passed: closed-scope forks do not execute, scoped acquisition releases once, and schema decoding rejects invalid input. These checks do not rerun the full earlier audit or establish general skill effectiveness.

## Previous Baseline

On 2026-10-18, the npm registry's `latest` release was Effect 4.0.5. The official `effect@4.0.5` release tag resolves to `7f524e25cfb49a71ac39b0f44278d08d40dda5de`. That revision pinned the reference checkout to that release. The skill verifies the latest stable release at task start, so this record is evidence for this revision rather than a permanent version requirement.

The earlier checkout at `0c8b446709c737c10d0e11af4313bb29fdff2588` also declared 4.0.5 but contained unreleased fixes. The audit reproduced differences in mixed-cause recovery, closed-scope forking, overlapping runtime disposal and the SqlClient after-commit API. The revised guides avoid assuming those unreleased guarantees and explicitly separate pull backpressure from push-source buffering.

## Retained Research

- [Historical provenance and validation](PROVENANCE.md) records the earlier skill, source revisions and executed-check limits.
- [Application studies](references/APPLICATIONS.md) preserve the original workflow evidence for maintenance.
- [Personal preferences](PREFERENCES.md) preserves optional style and migration choices outside the general guidance.

These optional clones are not installation dependencies and are left unchanged:

| Research source | Repository | Local checkout | Studied revision |
| --- | --- | --- | --- |
| OpenCode v2 | https://github.com/anomalyco/opencode | `repos/opencode` | `4617210822bdbb31e5749751afbfb4584ccedac8` |
| T3 Code | https://github.com/pingdotgg/t3code | `repos/t3-code` | `2fbd4318fc5b610c3e7fcfcbd5bbd80b73521d8f` |
| Alchemy | https://github.com/alchemy-run/alchemy | `repos/alchemy` | `9e3c0584342d67b24a4215f931047aabd230327b` |

Historical source links follow the current local checkouts. Recheck their recorded revisions before using them to establish a claim. Fetch research sources separately and review implementation and assertions before updating a study.

## Maintaining General Guidance

Verify the current stable registry release and its official source tag. Use the published package to compile runnable examples and probe uncertain behavior. Keep companion dependencies compatible. The sync script fetches default branches for review while preserving adopted checkouts; advancing Effect's adopted pin is a separate release-based update.

Keep transferable decisions in the skill, with each mechanism conditional on its caller contract. Keep source studies, narrow regression histories and optional preferences here. The installed skill should have no links into this directory or hardcoded workstation paths.

A source audit or passing helper test does not establish general skill effectiveness. When evaluating future changes, use unrelated consumer tasks across small programs, reusable APIs and framework integrations. Judge behavior, inferred types and unnecessary machinery; distinguish inspected source, executed checks and independent agent evaluation.

## Validation Of The 4.0.5 Revision

The four embedded TypeScript examples compiled against published Effect 4.0.5 with strict TypeScript 6.0.3. Six runtime checks passed with Node 24.21.0, `@effect/vitest` 4.0.5 and Vitest 5.0.4: the documented virtual-time example, service adapter substitution and error identity, schema rejection before I/O, scoped listener disposal, interruption cleanup, and explicit callback-stream capacity and release. The checks ran in an isolated temporary workspace.

Collection validation, seven validator tests, nineteen setup tests, installed-link/source-pin checks, archive-link checks, shell syntax and skill frontmatter validation passed. An isolated Git fixture also exercised the source-sync script: missing sources clone at adopted pins, and subsequent fetches preserve all four adopted checkouts, including Effect.

The installed skill now contains 4,245 words across its entrypoint and eight guides, compared with 15,915 words across the earlier skill and its research material. Its entrypoint is 391 words. These are document sizes, not measurements of tokens loaded in an individual task.

These checks validate examples, documentation and maintenance behavior. No new independent agent evaluation was run, so this revision does not establish a general skill success rate.
