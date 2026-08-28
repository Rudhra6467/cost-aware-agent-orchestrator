# CAOS — Cost-Aware Agent Orchestration System

Find the **lowest practical cost** path from an idea to a working local slice.

CAOS is not "the cheapest builder in the world." It is a planner that uses recorded free quota first, shows assumptions, then lets you choose:

1. **SHOW ME HOW** — a DIY roadmap file
2. **BUILD** — a local workspace with plan, audit, and artifacts

v0 BUILD uses the local deterministic agent. Actual model spend is $0 until a provider adapter exists.

## Run it

```bash
python -m pip install -e ".[dev]"
python run_server.py
```

Open http://127.0.0.1:8080

Use this test idea:

> Build a small Python API that stores customer notes and exposes a search endpoint.

Then click **Plan with CAOS**, then **SHOW ME HOW** or **BUILD**.

- DIY files land in `workspaces/diy/`
- BUILD workspaces land in `workspaces/<session_id>/`

## What is ready for testing

- Idea to two plans (Zero-Cost First, Lowest Practical Cost)
- Assumptions that say estimate is not actual
- SHOW ME HOW writes markdown
- BUILD writes `plan.json`, `roadmap.md`, `audit.json`, `status.json`, and task artifacts
- BUILD reports estimated vs actual cost

## What is not ready

- Live provider adapters
- Live free-tier probes
- Compiling production apps from arbitrary ideas
- n8n

## Tests

```bash
pytest -q
```

## Promise

Free-first. Paid capacity only as itemized spillover. Human gate before BUILD. Verification over agent claims.
