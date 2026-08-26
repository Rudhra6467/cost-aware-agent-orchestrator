# 21 — Cost-Aware Routing

CAOS now has a provider-neutral routing layer that combines task capability, reliability, price, and live health.

## Decision model

```text
feasible resources
      ↓
capability threshold
      ↓
context requirement
      ↓
budget constraint
      ↓
provider health/quota
      ↓
quality + reliability
      ↓
expected practical cost
      ↓
transparent route decision
```

The first implementation uses an intentionally simple score:

`quality = 0.6 * capability + 0.4 * reliability`

`expected_cost = estimated_cost + handoff_penalty * (1 - reliability)`

`route_score = quality / (1 + expected_cost)`

These weights are configuration candidates, not scientifically validated constants.

## Product principle

CAOS should not advertise "always free" or "always cheapest." It should identify the **lowest practical cost** that satisfies the user's quality, functionality, time, and legitimacy constraints.

## Next engineering step

Connect this router to the task DAG so every task gets an auditable routing decision, then record actual tokens, latency, retries, handoffs, and outcome. Those observations become the evidence base for learning better routing policies.
