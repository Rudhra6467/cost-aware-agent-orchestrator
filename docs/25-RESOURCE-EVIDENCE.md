# 25 — Resource Evidence Model

CAOS must distinguish a provider claim from verified operational evidence.

## Evidence record

Each resource record carries:

- provider and resource identity
- capabilities
- quality and reliability estimates
- context capacity
- input/output pricing
- free-tier notes
- availability status
- evidence URL
- last verification date
- confidence score

## Freshness policy

A resource is not permanently "free" or "available" merely because an old source says so. CAOS therefore supports a configurable freshness window and can exclude stale evidence from routing.

## Future evidence sources

1. Official provider pricing and quota documentation.
2. Official API responses and rate-limit headers.
3. CAOS execution telemetry.
4. Repeated benchmark results.

Community reports may be useful for discovery, but should not become authoritative pricing or quota evidence without corroboration.

## Routing principle

The optimizer should prefer a verified free resource when it satisfies the task's capability, quality, reliability, context and time constraints. Stale or low-confidence evidence should reduce trust rather than silently being treated as current fact.
