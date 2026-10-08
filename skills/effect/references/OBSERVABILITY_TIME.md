# Observability And Time

Read the applicable section when introducing operational telemetry or time-dependent behavior. Verify exact APIs and adapters through [SOURCE_WORKFLOW.md](SOURCE_WORKFLOW.md).

## Observe Owned Operations

Name useful application spans after the operation, such as `Checkout.processCheckout`. Use named `Effect.fn` at those boundaries; a pure helper or hot library loop may use an untraced function. Add child spans when they distinguish meaningful external calls or phases, not merely because a helper exists.

Attach structured log/span attributes with identifiers that help correlate the work. Keep credentials, secrets, and private payloads out of telemetry. Report expected failures, defects, and interruption according to their actual meaning; cancellation should retain its cancellation semantics. Avoid duplicate reporting at every layer of one failure.

Configure loggers, tracing exporters, and metrics at the application composition boundary, with acquisition and shutdown owned by that layer/runtime. Exporter transports and serializers are dependencies of that composition. Follow the installed version's adapters and the project's existing telemetry stack; upstream examples include lightweight OTLP layers and an OpenTelemetry integration.

Choose metrics for an operational question: counts, durations, distributions, or current state. Keep dimensions bounded; request IDs and unrestricted user input belong in diagnostic context rather than metric labels. Inspect `Metric.ts`, the relevant exporter, and tests before relying on aggregation/export details.

Canonical application examples:

- `ai-docs/src/08_observability/10_logging.ts`: logger layers, log levels, structured annotations, batching, and log spans.
- `ai-docs/src/08_observability/20_otlp-tracing.ts`: service spans and an application-owned exporter composition.

For exporter lifecycle questions inspect `packages/effect/src/observability`, `packages/opentelemetry`, and focused tests. Use the consuming application's configuration and test tools to verify the changed telemetry path.

## Time Is A Dependency

Use Clock-backed current time inside Effect workflows so tests can control it. Prefer `DateTime` for parsing, formatting, zone conversion, and calendar arithmetic; convert to native `Date` only at integrations that require it. Keep sleeps and recurring execution in Effect scheduling.

Distinguish an instant, a duration, a local date/time, and a time zone in the domain contract. Choose whether a calendar operation uses UTC or a named zone; make that choice explicit at input, storage, and presentation boundaries. A fixed offset alone does not describe a zone's daylight-saving rules.

Parse unknown timestamps and zones through a validated boundary. Use safe parsing results when invalid input is expected; unsafe constructors require an already-established invariant. Define intentional handling for ambiguous or nonexistent local times when the feature encounters them. Inspect the relevant DateTime/Cron implementation and tests for that policy rather than guessing it from a name.

Canonical examples:

- `ai-docs/src/07_datetime/10_creating-and-formatting.ts`: `DateTime.now`, safe construction, arithmetic, and ISO formatting.
- `ai-docs/src/07_datetime/20_time-zones.ts`: named zones and the current-zone service.

For elapsed-time measurement inspect the Clock API; for calendar recurrence inspect `Cron.ts`; for retries, polling, and deadlines read [SCHEDULING.md](SCHEDULING.md). Verify time-dependent behavior with [TESTING.md](TESTING.md), advancing virtual time after the work is waiting. Include time-zone transitions when they are part of the requested contract.

These design defaults are synthesized from the examples and source at the revisions in [PROVENANCE.md](../PROVENANCE.md); exact constructors and policies remain source lookups.
