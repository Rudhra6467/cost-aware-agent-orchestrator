# 56 — Unified Execution Planner V1

CAOS now exposes a single planner that starts from one task graph and produces the standard execution-plan variants used by the product experience.

## Standard variants

- **Zero-Cost** — maximize free-resource usage.
- **Lowest-Practical-Cost** — minimize practical execution cost subject to constraints.
- **Fastest-Practical** — optimize for delivery time when speed is important.

V1 establishes the common API and simulates the shared task graph. The resource-policy generation for each variant remains intentionally explicit rather than pretending that all three are already independently optimized.

## Current output

`UnifiedPlan` contains:

- a ranked `PlanComparison`;
- simulated schedule information;
- a recommendation ID and rationale.

## Important honesty rule

V1 does **not** claim that the three variants have different resource allocations yet. They currently share the optimizer baseline while the variant-policy layer is being implemented. This prevents the product from displaying fabricated savings or timing differences.

## Next milestone

Implement **Variant Policy Generation**. Generate genuinely different resource policies for Zero-Cost, Lowest-Practical-Cost and Fastest-Practical, then run each through the same quota-aware, dependency-aware simulator. Only then should the UI advertise distinct prices/timelines.
