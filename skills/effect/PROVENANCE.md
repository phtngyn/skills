# Effect Provenance

This is a personal guide derived from Effect's source and application examples. It contains synthesized decision guidance, conditional references, and source-navigation instructions; it does not install upstream contributor skills or require their release workflow in applications.

## Revisions And Authority

- Original API guides and selected examples were checked against Effect 4.0.1 at [`b1d200c40a1dad69def51ebdbf0a1a612a12b8ac`](https://github.com/Effect-TS/effect/tree/b1d200c40a1dad69def51ebdbf0a1a612a12b8ac).
- Naming, module design, agent workflow, testing branches, observability, and time guidance were reviewed against the local 4.0.1 checkout at [`757821fe99b7179f907d6d1a34a4e86de4173112`](https://github.com/Effect-TS/effect/tree/757821fe99b7179f907d6d1a34a4e86de4173112).
- The collection's [UPSTREAM.md](../../UPSTREAM.md) records the extraction baseline and fetched revision. This records material considered, not an exhaustive audit of every API or intervening fix.

The consuming project's installed package and compatible source remain authoritative for API facts. A reference checkout may be newer; a shared version string alone is insufficient. Fetching does not refresh these written summaries or authorize upgrading an application.

## Source Map

| Material | Primary source at the reviewed revision |
| --- | --- |
| Targeted local evidence workflow | [Effect development skill](https://github.com/Effect-TS/effect/blob/757821fe99b7179f907d6d1a34a4e86de4173112/.agents/skills/effect-development/SKILL.md), `LLMS.md`, `ai-docs/src` |
| Application services, layers, and functions | `ai-docs/src/01_effect/03_services`, `01_effect/01_basics/02_effect-fn.ts` |
| Complete application boundaries | `ai-docs/src/51_http-server/fixtures` and `04_integration/10_managed-runtime.ts` |
| Library models, combinators, and types | `packages/effect/src/Ref.ts`, `Request.ts`, `Function.ts`, `http/HttpClient.ts`, and focused tests/type tests |
| Imports and mechanical style | `packages/tools/oxc/oxlintrc.json`, `.oxlintrc.json`, `dprint.json`, and public module imports |
| Runtime versus compiler verification | [Test development skill](https://github.com/Effect-TS/effect/blob/757821fe99b7179f907d6d1a34a4e86de4173112/.agents/skills/test-development/SKILL.md), its runtime/type branches, `packages/vitest` |
| Public API documentation | `.agents/skills/jsdocs` and current public declarations |
| Telemetry and time | `ai-docs/src/08_observability`, `07_datetime`; `Metric.ts`, `DateTime.ts`, corresponding tests |
| Monorepo validation and generated files | [.agents/AGENTS.md](https://github.com/Effect-TS/effect/blob/757821fe99b7179f907d6d1a34a4e86de4173112/.agents/AGENTS.md) and the task-relevant contributor skill |

Topic guides retain their own more specific anchors. Paths refer to the selected Effect checkout, not to files bundled inside this skill.

## Personal Decisions

The principle names in the entry point are our synthesis, not upstream named principles. Applications are the default; library design loads only for reusable public contracts. Existing project conventions and the user's task govern adoption of style and architecture.

The plain-record preference for `Schema.Struct` plus a same-name interface is a retained personal choice. Upstream also uses class schemas. The domain-oriented organization advice cites [Structure an Effect codebase by domain](https://ratstack.sh/lore/structure-effect-by-domain); its broader house conventions are optional and are not Effect requirements.

## Updating

Compare the recorded baseline to the proposed source revision. Inspect relevant examples, declarations, tests, and changed conventions before adopting guidance. Update the extraction record with the material actually considered, and compile or execute examples whose API usage changes. Keep one home for each rule and replace stale API catalogs with precise source pointers where practical.

Runtime lookup of a compatible local checkout does not require changing this extraction baseline. Prefer narrow retrieval and reuse verified evidence within the task.
