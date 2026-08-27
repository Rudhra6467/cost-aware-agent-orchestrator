# 57 — Variant Policy Generation V1

CAOS now has explicit optimization policies for the three standard plan variants.

## Zero-Cost

Strongly prioritizes currently available free capacity. Paid spillover is strongly penalized.

## Lowest-Practical-Cost

Balances paid spend with quality and reliability, while still benefiting from free quota.

## Fastest-Practical

Uses a different policy emphasizing reliable/high-quality resources and is designed to become time-aware as provider latency/concurrency data is added.

## Design rule

The three labels are only meaningful if their underlying allocation policies differ. V1 therefore generates allocations independently for each policy instead of copying one baseline result and renaming it.

## Current limitation

Speed is not yet a direct measured provider attribute in the resource model, so the fastest policy currently uses reliability/quality as proxies. This must be replaced with observed latency, concurrency and queue data before CAOS makes strong speed claims.

## Next milestone

Connect these policy-generated allocations to the dependency-aware simulator and quota scheduler, then calculate variant-level cost, waiting time, free usage, reliability and critical-path duration for an evidence-backed comparison.
