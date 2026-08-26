# 29 — Cost Arbitrage V1

CAOS now has a provider-neutral bridge from resource evidence to task routing.

## Flow

```text
Task
  ↓
required capability
  ↓
ResourceDiscovery
  ↓
remove unavailable/stale evidence
  ↓
compare estimated unit cost
  ↓
choose lowest-cost eligible resource
  ↓
execute
```

## Fail-closed principle

If CAOS has no fresh evidence for a capable resource, routing does not invent a provider, price, quota, or free tier. It returns a controlled failure so discovery can be refreshed or the user can be informed.

## Important distinction

This is **cost arbitrage**, not simply "pick the free model." A $0 resource is useful only when it is capable, available, and supported by sufficiently fresh evidence. Later versions will add task quality thresholds, historical reliability, quota remaining, expected latency, switching/handoff cost, and budget constraints.

## Next step

Connect the decision object to the existing execution planner and record the selected resource plus evidence provenance in execution telemetry. Then add a real trusted source adapter.
