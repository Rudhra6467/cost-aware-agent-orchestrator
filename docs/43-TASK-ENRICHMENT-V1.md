# 43 — Task Enrichment V1

CAOS now has a structured contract for turning a baseline DAG task into an optimization-ready task.

## Enriched task

Each task carries:

- capabilities required;
- security requirements;
- acceptance tests;
- estimated input tokens;
- estimated output tokens;
- expected tool calls.

## Architecture

```text
Project idea
  ↓
Blueprint
  ↓
Project-aware DAG
  ↓
Task enrichment
  ↓
Deterministic validation
  ↓
Resource matching
  ↓
Cost optimization
```

The V1 implementation is deliberately deterministic. A future LLM enrichment adapter can propose richer descriptions, capabilities and tests, but its output must satisfy the same validation contract before entering the optimizer.

## Why this matters

Resource selection needs task-level information. “Coding” is too broad to optimize well. CAOS eventually needs to distinguish React implementation, database migration, payment integration, security review, test repair, research, UI generation and similar workloads.

## Next research step

Implement a provider/resource registry and a live research adapter. The enriched task should be matched against resource capabilities, pricing, free quota, reliability evidence and security constraints to generate concrete Zero-Cost and Lowest-Practical-Cost plans.
