# 49 — Global Optimizer V1

CAOS now has a whole-project optimization baseline rather than treating each task as an independent cost decision.

## What it does

`GlobalOptimizer` receives the complete enriched task set, ranks constrained tasks first, considers all eligible resources, and uses the shared `UsageLedger` while assigning capacity.

For each candidate it estimates:

- units required;
- free units still available;
- paid spillover;
- resulting cost;
- quality/reliability-adjusted candidate cost.

The result explicitly reports assignments, total cost, whether the project is fully free, and tasks with no eligible resource.

## Why this matters

The optimization problem is now moving from:

> cheapest resource for this task

toward:

> cheapest feasible allocation for this set of tasks under shared resource constraints.

## V1 limitations

This is a deterministic heuristic, not a mathematical proof of global optimality. It does not yet model:

- DAG dependency ordering as an optimization constraint;
- parallelism and elapsed build time;
- retries and failure probability as expected cost;
- quota reset windows;
- context-transfer cost;
- task quality thresholds beyond candidate filtering;
- provider switching overhead;
- multi-resource tasks;
- user budget as a hard constraint.

Those become the next optimization layers.

## Next milestone

Build the **User Constraint & Plan Explanation layer**. CAOS needs explicit budget, quality, time and autonomy constraints, then it should explain why each assignment was chosen and surface trade-offs rather than returning an opaque score.
