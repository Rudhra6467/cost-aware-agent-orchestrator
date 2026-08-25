# 17 — Resource Registry V1

## Purpose

Create a small, evidence-backed registry before attempting automated discovery. This lets the optimizer operate on structured data and gives us a reproducible baseline for research.

## Initial Schema

```text
resource_id
provider
name
category
capabilities
quality_score
reliability_score
context_capacity
input_cost
output_cost
free_tier_notes
quota_notes
availability_status
latency_score
terms_notes
evidence_url
last_verified_at
confidence
```

## Registry Rules

1. No pricing or quota claim without evidence.
2. Volatile fields require `last_verified_at`.
3. Separate advertised limits from observed behavior.
4. Separate resource availability from user eligibility.
5. Never represent a free tier as unlimited.
6. Prefer official provider documentation for pricing and limits.
7. Record uncertainty rather than inventing values.
8. Keep the registry provider-neutral.

## V1 Scope

Start with a deliberately small set of resources sufficient to demonstrate routing:

- at least two LLM/API resources,
- at least one open-source/local option,
- at least one coding/development resource,
- at least one backend/database option,
- at least one hosting option.

The registry is a research instrument, not a complete catalog.

## Future Versions

V2: automated evidence refresh.

V3: measured benchmark integration.

V4: dynamic resource discovery and change detection.

V5: user-specific eligibility and quota state where legitimately available.
