# 34 — Performance Evidence V1

CAOS now has a normalized representation of historical execution outcomes.

## Recorded outcome

Each execution records:

- resource ID;
- success/failure;
- verification pass/fail;
- actual cost;
- latency;
- retry count.

## Derived evidence

CAOS can aggregate outcomes per resource into:

- execution count;
- success rate;
- verification rate;
- average cost;
- average latency;
- average retries.

## Why this matters

Provider claims and pricing pages tell CAOS what a resource *should* cost or support. Execution evidence tells CAOS how the resource actually behaves in this workload.

The mature optimizer should combine both:

`observed price + observed reliability + observed verification success + expected retry/handoff cost`

rather than optimizing advertised token price alone.

## Research implication

This creates the measurement layer needed to test whether cost-aware routing actually reduces **practical cost per verified successful task**.
