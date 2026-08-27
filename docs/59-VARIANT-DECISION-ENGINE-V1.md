# 59 — Variant Decision Engine V1

CAOS now has an explicit, transparent decision layer over evaluated plan variants.

## Decision inputs

- variant monetary cost;
- simulated execution time;
- quota waiting time;
- user budget constraint;
- user maximum-duration constraint.

## Behavior

1. Filter plans that violate explicit user constraints.
2. If feasible plans exist, rank those plans.
3. If none are feasible, return the lowest-practical-cost fallback and clearly state that constraints could not all be satisfied.
4. Return structured reasons and a human-readable explanation.

## Why this matters

The recommendation is now a deterministic product decision rather than an opaque model-generated opinion. An LLM can later improve explanation wording, but it must not silently override the decision policy.

## Current V1 ranking

Among feasible plans, CAOS minimizes:

1. expected monetary cost;
2. quota waiting time;
3. simulated execution duration.

Future versions can make these priorities user-configurable and incorporate measured reliability, quality, success probability and developer-time value.

## Next milestone

Create the **Planning API / end-user contract** that turns a raw idea plus user constraints into a stable response containing blueprint, assumptions, evidence, three plans, recommendation, and explicit next actions: `BUILD` or `DIY`.
