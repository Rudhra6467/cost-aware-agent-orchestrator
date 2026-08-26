# 36 — Quota-Aware Routing V1

CAOS now models known quota and rate-limit state and incorporates it into resource selection.

## Quota state

A resource can expose:

- configured limit when known;
- usage;
- remaining capacity;
- reset timestamp;
- explicit limited/exhausted state.

Unknown limits are supported. CAOS does not invent a quota number.

## Routing behavior

An exhausted or explicitly rate-limited resource is not eligible for execution. Among otherwise eligible resources, expected practical cost remains the primary objective, with healthier quota used as a secondary preference.

```text
Capability
   ↓
Quality / security
   ↓
Historical reliability
   ↓
Quota availability
   ↓
Expected practical cost
   ↓
Resource selection
```

## Strategic significance

This is the first implementation of CAOS's free-tier arbitrage concept at the routing layer. Future versions should understand daily/weekly/monthly windows, reset schedules, concurrency limits, token budgets, trial expiration, and projected quota consumption for an entire task DAG.

## Safety principle

Quota information is evidence, not permission to circumvent provider controls. CAOS must use documented APIs and normal provider limits and must never evade rate limits or abuse free-tier systems.
