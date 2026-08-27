# 51 — Plan Comparison Engine V1

CAOS now compares alternative execution plans against explicit user constraints instead of presenting a single opaque answer.

## Supported inputs

Each variant can contain:

- optimization result;
- estimated build duration;
- plan name and ID.

User constraints include budget, quality threshold, maximum build time, autonomy preference and free-resource preference.

## Ranking policy

V1 treats budget, time and unfulfilled tasks as feasibility constraints. Among feasible options it prefers:

1. lower estimated cost;
2. greater free-capacity coverage;
3. shorter estimated build time.

The engine returns the ordered variants, a recommended variant ID and a human-readable rationale.

## Product behavior

This creates the foundation for the end-user comparison screen:

```text
ZERO-COST       $0       8 days
HYBRID          $2.40    5 days   ← recommended
FASTEST         $8.10    2 days
```

The recommendation must always be explainable and should never claim that a heuristic is a mathematical proof of cheapest possible execution.

## Next milestone

Add **Execution Strategy Modeling**: estimate retries, context handoffs, latency, parallelism and provider-switching overhead so CAOS can compare not just monetary cost but total practical execution cost.
