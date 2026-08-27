# 45 — Resource Evidence V1

CAOS now separates resource facts from the evidence supporting those facts.

## Evidence record

Every research observation can record:

- resource ID;
- source URL;
- source type;
- observed timestamp;
- the specific claim observed;
- confidence.

The registry can retrieve all evidence for a resource and select the freshest observation.

## Why provenance is mandatory

Pricing, quotas, model availability and free tiers change. CAOS must not treat a resource record as timeless truth. The optimizer should eventually be able to say both **what** it believes and **when/how** that belief was verified.

## Research architecture

```text
Provider documentation / trustworthy source
                    ↓
             Research adapter
                    ↓
             Evidence record
                    ↓
             Resource registry
                    ↓
             Capability matcher
                    ↓
             Cost optimizer
```

## Important limitation

V1 stores provenance but does not yet crawl or automatically refresh external provider data. Live research and refresh policies are the next layer.

## Next step

Implement capability matching between `EnrichedTask` and `ResourceRegistry`, including minimum quality and security requirements, then produce ranked candidates with evidence freshness and confidence.
