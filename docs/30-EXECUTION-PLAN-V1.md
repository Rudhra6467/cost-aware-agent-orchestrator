# 30 — Execution Plan V1

CAOS now converts evidence-backed resource decisions into a provider-neutral execution plan.

## Plan structure

Each planned task records:

- task ID;
- selected resource;
- provider;
- estimated cost;
- evidence confidence;
- evidence source;
- human-readable rationale.

The plan also exposes an estimated total cost before execution.

## Why this matters

The user-facing promise requires a proposal **before** CAOS spends resources. The execution plan is the bridge between that proposal and actual execution.

```text
Idea → DAG → Resource Evidence → Cost Arbitrage → Execution Plan → User Approval → Execution
```

## Current limitation

V1 chooses the lowest-cost fresh capable resource. It does not yet optimize globally for quota exhaustion, quality thresholds, latency, retry probability, handoff cost, or dependency scheduling. Those belong in the next optimizer iterations.

## Design principle

Every cost decision must remain explainable: CAOS should be able to tell the user which resource it selected, what evidence supported the selection, the estimated cost, and why a more expensive resource was not selected.
