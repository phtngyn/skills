# Historical Personal Preferences

These preferences were retained from the earlier skill. They are outside the installed general skill and are not automatically applied. Use them only when requested by the user or established by the consuming project.

- For ordinary records, prefer `Schema.Struct` with a same-name interface; use classes when constructor behavior or class identity helps.
- For schema-backed error classes, a per-class type brand can prevent structural substitutes. This is an optional nominal typing contract, not a requirement for tagged errors. Its runtime and type checks belong to a feature that actually needs that guarantee.
- For an authorized internal refactor, migrate affected callers and remove the superseded implementation together, avoiding compatibility scaffolding whose only purpose is to retain the old internal design. Public, persisted and externally consumed contracts require their own migration policy.

The general skill chooses model shape, inference and migration strategy from the current task's requirements and project conventions.
