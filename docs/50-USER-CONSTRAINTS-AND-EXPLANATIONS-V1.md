# 50 — User Constraints & Plan Explanations V1

CAOS must optimize for the user's actual definition of "best," not cost alone.

## User constraint model

V1 captures:

- maximum monetary budget;
- minimum quality threshold;
- optional maximum build time;
- autonomy preference: controlled, autonomous, or DIY;
- preference for free resources.

## Why this matters

Two users with the same idea can legitimately receive different plans.

```text
User A: $0 budget + DIY
User B: $5 budget + autonomous
User C: $50 budget + fastest practical build
```

The optimizer should not pretend these are the same problem.

## Explanation layer

`PlanExplainer` converts an optimization result into user-facing information:

- headline;
- summary;
- recommendation;
- cost/free-capacity trade-offs;
- warnings for budget overruns or unfulfilled tasks.

This is intentionally separate from the optimizer. The optimizer makes decisions; the explanation layer makes those decisions understandable.

## North Star

The product promise is **Build your idea for the lowest practical cost.** The word *practical* includes the user's budget, quality expectations, time constraints and desired autonomy.

## Next milestone

Build the **Plan Comparison Engine**: generate Zero-Cost, Lowest-Practical-Cost and (when useful) Fastest-Practical variants, compare them against user constraints, and produce a recommendation with explicit reasons.
