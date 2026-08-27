# 46 — Task → Resource Matching V1

CAOS now connects optimization-ready tasks to eligible resources.

## Input

An `EnrichedTask` supplies required capabilities and token/tool estimates. The `ResourceRegistry` supplies provider capabilities, price, free capacity, quality and reliability. The `EvidenceRegistry` supplies provenance and freshness.

## Output

Each task receives ranked `ResourceCandidate` records containing:

- resource;
- evidence count;
- freshest evidence age;
- evidence confidence.

## Ranking principle

V1 uses a transparent baseline:

1. available free capacity;
2. reliability-adjusted unit cost;
3. quality;
4. reliability;
5. evidence freshness.

This ranking is deliberately not the final optimizer. A resource can be cheap but unsuitable, stale, unreliable, or incapable of satisfying the full task. Future versions will incorporate hard constraints, quota consumption, security requirements, expected retries, latency, lock-in, and task-specific quality thresholds.

## Important distinction

The matcher identifies candidates; it does not yet claim that a candidate is the globally cheapest feasible solution. That decision belongs to the planner/optimizer after all task dependencies and resource constraints are considered.

## Next milestone

Build the **Zero-Cost / Lowest-Practical-Cost Plan Generator**, which selects resources across the complete DAG, accounts for free capacity and dependencies, and produces a transparent user-facing comparison.
