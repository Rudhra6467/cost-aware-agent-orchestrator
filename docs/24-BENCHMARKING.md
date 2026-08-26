# 24 — Benchmarking CAOS

## Purpose

The CAOS claim must be measurable. We therefore compare CAOS against a fixed routing baseline using the same task DAG, requirements, verification criteria and run count.

## Primary metrics

- Total cost
- Average cost per successful run
- Success rate
- Verification pass rate
- Average latency
- Retries
- Handoffs

## Primary comparison

`cost_savings_pct = (baseline_total_cost - caos_total_cost) / baseline_total_cost × 100`

Quality must never be hidden behind the cost number. A cheaper system that produces materially worse software is not a successful CAOS result.

## Experimental discipline

For each benchmark:

1. Freeze the task DAG.
2. Freeze requirements and acceptance tests.
3. Use the same available resource set.
4. Run a fixed baseline policy.
5. Run the CAOS policy.
6. Record actual telemetry, not estimates.
7. Repeat enough times to reduce single-run noise.
8. Report cost, quality, reliability and latency together.

## First benchmark target

Use a small deterministic application with a backend API, persistence, tests and a minimal interface. This keeps execution cost low while exercising decomposition, routing, verification and recovery.

## Important limitation

Synthetic benchmark numbers are not product claims. We need repeated real-provider measurements before advertising quantified savings.
