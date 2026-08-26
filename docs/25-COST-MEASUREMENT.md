# 25 — Cost Measurement Contract

CAOS must distinguish **estimated cost** from **actual cost**.

## Normalized execution record

Every provider adapter should eventually produce:

- provider/resource identifier
- input tokens
- output tokens
- total tokens
- estimated cost
- actual cost when the provider exposes sufficient billing/usage information
- latency
- success/failure
- retry count
- handoff count
- timestamp

## Why this matters

Provider pricing is heterogeneous. CAOS therefore converts provider-specific usage into a common internal representation before optimization and benchmarking.

## Decision rule

A resource is not considered cheaper merely because its published price is lower. CAOS should prefer a lower-cost resource only when it remains inside the task's minimum quality, reliability, security and functionality constraints.

## Future calibration

After enough real observations, CAOS can calculate prediction error by resource and use that evidence to improve future estimates. Calibration must not override hard user constraints.
