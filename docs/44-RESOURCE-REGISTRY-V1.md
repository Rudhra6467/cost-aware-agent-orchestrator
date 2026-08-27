# 44 — Resource Registry V1

## Purpose

The Resource Registry is the normalized inventory CAOS uses when deciding how a task can be completed. It deliberately separates resource facts from routing decisions.

## Resource record

Each resource currently represents:

- provider and resource identity;
- capabilities;
- billing unit;
- nominal unit cost;
- included/free units;
- reliability evidence;
- quality score;
- freshness age;
- enabled state.

## Matching

A task capability is matched only against enabled resources meeting the task's minimum quality. Candidates are ordered by reliability-adjusted unit cost, then quality and reliability.

This is **not yet live ecosystem research**. The registry is the normalization boundary. A future research adapter will populate it from documented provider pricing, quota and capability evidence and attach timestamps/source evidence.

## Cost principle

CAOS must distinguish:

1. nominal price;
2. included free capacity;
3. expected cost after reliability/retry effects;
4. practical cost under the user's constraints.

A $0 resource remains preferable when it satisfies the task and has available free capacity. A paid resource becomes a candidate only when it provides a legitimate capability or avoids a meaningful bottleneck.

## Next step

Connect enriched tasks to registry matching and introduce a source/evidence model so resource records can be refreshed without treating stale pricing as current truth.
