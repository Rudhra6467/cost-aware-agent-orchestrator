# 22 — Task Routing & Telemetry

CAOS now connects the dependency-aware task layer to cost-aware resource selection and introduces the telemetry model required to validate the product thesis.

## Execution loop

```text
Task DAG
  ↓
ready tasks only
  ↓
capability + context filtering
  ↓
provider health
  ↓
cost-aware routing
  ↓
execution
  ↓
verification
  ↓
telemetry
  ↓
future routing evidence
```

## Telemetry captured

- run/task/provider identifiers
- estimated and actual cost
- input/output tokens
- latency
- retries
- handoffs
- verification outcome
- timestamp

## Why this matters

The product claim is not "CAOS uses free AI." The claim is that CAOS finds a lower practical cost while satisfying user constraints. That cannot be established without measuring actual execution outcomes.

## Next milestone: M2 — Evidence-Driven Resource Intelligence

1. Persist telemetry in SQLite.
2. Add provider resource records with evidence timestamps and source URLs.
3. Add quota-window accounting rather than a static `remaining_requests` field.
4. Record actual provider responses and normalize usage metadata.
5. Compare predicted cost vs actual cost.
6. Add benchmark runs against fixed routing baselines.
7. Feed measured reliability and cost back into routing.
