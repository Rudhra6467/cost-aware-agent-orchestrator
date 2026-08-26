# 28 — Resource Discovery V1

## Purpose

Resource Discovery provides the optimizer with evidence about candidate AI/software resources. V1 deliberately separates **observation** from **selection**.

## Observation record

Each observation contains:

- resource identifier;
- provider;
- capabilities;
- evidence source;
- observation timestamp;
- free/paid classification;
- estimated unit cost;
- confidence;
- availability.

## Freshness rule

A resource observation is not treated as current after its configured maximum age. The default V1 freshness window is 24 hours. This is intentionally conservative for quotas, availability, and pricing that can change.

## Selection rule

For a requested capability, V1 filters out unavailable and stale observations, then chooses the lowest estimated unit cost. Confidence is used as a deterministic tie-breaker.

## Important limitation

V1 is an evidence registry, not automated web scraping. Automated discovery should be added only with provenance, parsing validation, source-specific adapters, timestamps, and failure handling. CAOS must never invent a free tier, quota, or price when evidence is unavailable.

## Next step

Connect trusted source adapters and persist observations in the existing SQLite state layer. Then feed observed resource availability and cost into the optimizer.
