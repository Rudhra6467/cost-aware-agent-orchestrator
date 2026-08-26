# 33 — Constrained Optimization V1

CAOS must minimize practical cost **subject to the task remaining acceptable**.

## Constraint model

A task may specify:

- required capability;
- minimum quality;
- minimum reliability;
- maximum unit cost;
- minimum security level;
- functional acceptance criteria.

Resources are evaluated against these constraints before cost ranking.

```text
                 Candidate resources
                         ↓
                 Capability filter
                         ↓
                 Freshness filter
                         ↓
             Quality/reliability filter
                         ↓
                   Security filter
                         ↓
                    Cost ranking
                         ↓
               Cheapest eligible
```

## Key principle

A cheaper resource that fails the acceptance constraints is **not a cheaper solution**. It is an invalid solution.

This is the mathematical direction of CAOS:

`minimize expected practical cost subject to capability, quality, reliability, security, budget, and acceptance constraints.`

## V1 limitation

Quality and reliability are supplied as explicit evidence records rather than inferred from model names. V1 does not yet calculate these scores from historical benchmark outcomes. That is the next research layer.
