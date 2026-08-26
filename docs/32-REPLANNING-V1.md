# 32 — Replanning V1

CAOS should not stop at the first budget rejection. It should search for a cheaper verified execution path before asking the user for more money.

## V1 behavior

The replanner can select zero-cost work that is already represented in the approved plan. It deliberately does **not** invent a replacement provider or claim that an unverified free service is equivalent.

```text
Original Plan
    ↓
Budget Gate
    ↓
Rejected
    ↓
Replanner
    ↓
Verified cheaper subset / alternative
    ↓
Budget Gate again
```

## Why this is intentionally conservative

Dropping a paid task can make a plan cheaper but incomplete. V1 therefore labels this as a cheaper *candidate*, not proof that the original functionality has been preserved. Future versions must perform capability equivalence checks before substituting resources.

## Future optimizer

The mature replanner should evaluate substitutions, task splitting, local execution, batching, caching, quota windows, provider switching, and quality constraints while preserving the user's acceptance criteria.
