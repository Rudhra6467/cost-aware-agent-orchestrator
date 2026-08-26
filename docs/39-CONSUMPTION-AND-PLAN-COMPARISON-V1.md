# 39 — Consumption Estimation & Plan Comparison V1

CAOS now models pre-execution consumption and compares complete execution alternatives.

## Consumption

Each planned task can represent expected:

- input tokens;
- output tokens;
- API requests;
- tool calls.

This is intentionally provider-neutral. Provider adapters can later translate these units into provider-specific quota and price dimensions.

## Whole-plan comparison

CAOS can represent alternatives such as:

- zero-cost/free-first;
- hybrid low-cost;
- slower plan with more reset-window waiting;
- higher-reliability plan.

Each plan records estimated cost, wait time, risk, and verified-success probability.

The baseline ranker prioritizes lower estimated cost, then lower risk, then higher success probability, then lower wait time. A budget filter can eliminate plans above the user's hard budget.

## Product significance

This creates the foundation for CAOS's two-option user proposal:

**Option A — Let CAOS Build It:** select and execute the best feasible plan.

**Option B — Show Me How:** expose the selected plan as a reproducible DIY roadmap with resources, steps, expected cost, and assumptions.

## Research caution

The current ranker is deliberately transparent and deterministic. It is not yet a learned optimizer. Future work should compare ranking strategies experimentally using actual execution evidence and include switching, waiting, failure recovery, and verification costs.
