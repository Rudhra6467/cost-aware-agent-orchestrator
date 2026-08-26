# 23 — M2 Evidence & Telemetry

## Objective

Move CAOS from static resource assumptions toward measurable, time-aware resource intelligence.

## Implemented in this pass

- SQLite `TelemetryStore` for execution observations.
- Aggregate execution summary for actual cost, tokens, latency, retries and handoffs.
- `ResourceEvidence` records containing provider/model capability, prices, free quota, rate-limit description, source URL, observation timestamp and confidence.
- Evidence freshness checks.

## Operating rule

A provider being described as "free" is not a permanent fact. CAOS should retain the evidence source and observation time and treat stale evidence as lower confidence.

## Next implementation

1. Persist resource evidence in SQLite.
2. Add source-type and verification metadata.
3. Normalize provider-specific usage responses into telemetry.
4. Calculate predicted-vs-actual cost.
5. Build a benchmark runner with fixed baseline policies.
6. Compare CAOS against baseline routing on identical task DAGs.
7. Feed observed reliability/cost back into routing only after enough observations exist.
