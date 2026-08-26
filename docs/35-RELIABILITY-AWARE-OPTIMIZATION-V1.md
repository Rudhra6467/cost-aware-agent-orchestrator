# 35 — Reliability-Aware Optimization V1

CAOS now persists historical execution outcomes and can use them when selecting resources.

## Practical-cost model

V1 estimates the cost of a verified successful execution as:

`average_cost × (1 + average_retries) ÷ verification_rate`

A resource with zero verification success is assigned infinite expected practical cost and is excluded from reliable optimization.

## Routing hierarchy

```text
Fresh capability evidence
        ↓
Task quality/security constraints
        ↓
Historical execution evidence
        ↓
Expected practical cost
        ↓
Cheapest reliable candidate
```

## Important limitation

The formula is intentionally a first research baseline, not a claim of an optimal economic model. Real execution cost can include latency, failed work, context transfer, quota exhaustion, handoffs, infrastructure, and opportunity cost.

## Research metric

The key metric for experiments should be:

**Cost per verified successful task**

This provides a measurable comparison between naive cheapest-first routing, static provider selection, and CAOS adaptive routing.
