# 37 — Project Quota Forecasting V1

CAOS now forecasts whether planned usage will exhaust a known resource quota before the work executes.

## Model

For each resource:

`remaining_after = max(0, remaining_before - planned_units)`

The projection also records whether planned work exceeds currently available quota and how long until a known reset.

## Why this matters

Reactive routing waits for a 429. Forecasting lets CAOS avoid a predictable failure before execution begins.

```text
Planned DAG
   ↓
Expected resource usage
   ↓
Quota forecast
   ↓
Will quota survive the plan?
   ├── YES → resource remains eligible
   └── NO  → schedule/switch/replan
```

## V1 limitation

V1 forecasts aggregate planned units. It does not yet model time-ordered execution, reset windows, concurrency, or uncertain token consumption.

## Next evolution

Build a quota scheduler that can split work across providers and schedule work around documented reset windows while minimizing practical cost and preserving task dependencies.
