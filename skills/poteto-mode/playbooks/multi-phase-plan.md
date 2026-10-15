### Multi-phase or multi-PR plan

The plan is the deliverable. Do not implement until the user asks to execute it.

1. Ground the change in code, callers, requirements, and available checks. Use `how`, and `why` when history constrains the design. Settle observable uncertainties with a small prototype when authorized. Name any product decisions still needing the user.
2. Define the target state, scope, acceptance criteria, and relevant risks. Split work into small units with explicit dependencies and verification gates. Prefer scaffolding and the riskiest unknowns first. Use `architect` when the interface shape needs exploration.
3. Choose the execution route: Feature, Refactoring, or Bug fix for focused work; `figure-it-out` for one ambitious run; Orchestrate for a standing program; Autopilot-full only for an authorized merge queue; Autopilot-stack when the user will land the stack.
4. Write the plan to the requested path, or the project's established plans directory. Each unit names its goal, affected paths and owners, input dependency, observable result, exact check or live journey, evidence artifact, and completion condition. Include publication or review gates only where the task requires them.
5. Describe live verification for behavior changes. Use the project's harness or available control tools. State missing prerequisites and blocked coverage. For performance-sensitive work, name the metric, fair baseline, interleaved probe, and failure threshold. Avoid invented baseline values or mandatory performance lanes for work with no performance claim.
6. Specify writable isolation, integration ownership, concurrency limits, and how the next unit is released. Follow `references/codex.md`. Long work needs checkpoints and a decision log. A plan does not itself arm a timer or scheduler.
7. Review the dependency graph and each completion predicate. Check commands against the actual project and verify cited paths. Apply `technical-writing` and `unslop`. Report the plan path, dependency order, remaining decisions, and unverified prerequisites, then stop.

A useful unit template:

```markdown
## <Concrete change>

Depends on: <unit or none>
Owner and paths: <exclusive write scope>
Result: <observable behavior or structural outcome>

- [ ] <One implementation action>
- [ ] Run <actual check>, passing when <predicate>.
- [ ] Exercise <real user journey>, save <artifact>, passing when <predicate>.
- [ ] Complete <required review or delivery gate>.

Risks and prerequisites: <specific unresolved facts>
```
