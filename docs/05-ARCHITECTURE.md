# 05 — Architecture

## Product Architecture

```text
USER IDEA + CONSTRAINTS
        |
        v
   IDEA ANALYZER
        |
        v
   RESEARCH ENGINE
        |
        v
   TASK DECOMPOSER
        |
        v
  RESOURCE INTELLIGENCE
  capability | cost | availability | reliability | context | terms
        |
        v
   COST OPTIMIZER
        |
        v
   EXECUTION PLAN
       /       \
      /         \
     v           v
BUILD FOR USER   DIY ROADMAP
     |
     v
   TASK DAG
     |
     v
DYNAMIC AGENT/RESOURCE SELECTION
     |
     v
EXECUTION + CONTEXT HANDOFF
     |
     v
PERSISTENCE
 SQLite + Git/GitHub
     |
     v
VERIFICATION
     |
  +--+--+
  |     |
PASS   FAIL
  |     |
  v     v
NEXT   REPLAN / RETRY / HANDOFF
```

## Responsibility Boundaries

### Python Core

The authoritative orchestration engine: task modeling, planning policies, resource scoring, cost calculations, state transitions, DAG logic, telemetry, optimization experiments, and verification policies.

### n8n / Low-Code Integration Layer

Optional operational layer for visual workflows, webhooks, external API integration, branching, retries, notifications, and human approval. It must not contain irreplaceable business logic.

### Git/GitHub

Source code, project documentation, commits, branches, software artifacts, and reproducible project history.

### SQLite

Structured orchestration state: projects, tasks, resources, executions, tokens, costs, failures, handoffs, decisions, plans, and benchmark measurements.

## State Model

Git answers: **What happened to the software artifacts?**

SQLite answers: **What happened to the orchestration?**

The two stores complement rather than replace each other.

## Core Components

### 1. Idea Analyzer
Converts an unstructured user idea and constraints into structured requirements, assumptions, acceptance criteria, budget, quality target, and deadline.

### 2. Research Engine
Finds legitimate implementation resources and current constraints. It should eventually track providers, free tiers, trials, open-source alternatives, pricing, rate limits, capabilities, and last-verified timestamps.

### 3. Task Decomposer
Turns the requirements into a dependency-aware task graph (DAG), identifying which tasks can be parallelized and which require prior outputs.

### 4. Resource Intelligence
Maintains evidence-backed resource profiles rather than hard-coded provider preferences.

### 5. Cost Optimizer
Chooses the lowest practical execution strategy subject to functionality, quality, reliability, security, time, budget, and legitimate-use constraints.

### 6. Agent/Resource Selector
Selects the best available executor for each task using current resource state and task-specific evidence.

### 7. Context & State Manager
Preserves structured project state so work can move between agents when limits, failures, or cost conditions change.

### 8. Execution Engine
Runs tasks through provider-neutral adapters and records telemetry.

### 9. Verification Engine
Builds, tests, reviews, and validates outputs. A model's assertion of success is never sufficient evidence.

### 10. Recovery/Replanning Engine
Handles rate limits, timeouts, failed tests, invalid outputs, budget pressure, and unavailable resources by retrying, handing off, or replanning.

### 11. Delivery Engine
Produces either the built artifact or the detailed DIY roadmap, including cost and implementation assumptions.

## Initial Agent Roles

- Researcher — discovers resources and implementation options.
- Planner — decomposes requirements and dependencies.
- Architect — proposes system design.
- Developer — implements code.
- Reviewer — evaluates implementation and architecture.
- Tester — executes verification.
- Cost Optimizer — compares execution strategies.

Early versions may combine roles to minimize complexity.

## Dynamic Selection Inputs

The selection/optimization model should consider:

- task capability fit,
- measured quality/reliability,
- current availability,
- context capacity/fit,
- expected latency,
- input/output cost,
- remaining free quota where legitimately available,
- remaining project budget,
- handoff cost,
- expected failure/retry cost,
- implementation effort,
- provider terms/eligibility.

The scoring and optimization model is a research variable. It must be validated experimentally rather than treated as universally correct.
