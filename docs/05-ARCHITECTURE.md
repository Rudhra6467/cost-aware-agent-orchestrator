# 05 — Architecture

## Target Architecture

```text
USER / PROJECT BLUEPRINT
          |
          v
     META-PLANNER
          |
          v
 RESOURCE INTELLIGENCE
 capability | cost | availability | reliability | context
          |
          v
     COST OPTIMIZER
          |
          v
       TASK DAG
          |
   +------+-------+-------+
   |              |       |
 Planner       Developer Reviewer/Tester
   |              |       |
   +--------------+-------+
                  |
                  v
            STATE MANAGER
          SQLite + Git/GitHub
                  |
                  v
             VERIFICATION
                  |
             +----+----+
             |         |
           PASS       FAIL
             |         |
             v         v
         COMPLETE    REPLAN
```

## Responsibility Boundaries

### n8n
Visual workflow execution, webhooks, API integration, branching, retries, and operational visibility.

### Python
Agent scoring, planning policies, cost calculations, state transitions, DAG logic, telemetry, and experiments.

### Git/GitHub
Source code, project documentation, commits, branches, and software artifacts.

### SQLite
Structured orchestration state: projects, tasks, agents, executions, tokens, costs, failures, handoffs, decisions, and benchmark measurements.

## State Model

Git answers: **What happened to the software?**

SQLite answers: **What happened to the orchestration?**

## Initial Agent Roles

- Planner — decomposes requirements and dependencies.
- Developer — implements code.
- Reviewer — evaluates implementation and architecture.
- Tester — executes verification.

## Dynamic Selection Inputs

The initial scoring model will consider:

- task capability fit,
- expected reliability,
- current availability,
- context capacity/fit,
- expected latency,
- input/output cost,
- remaining project budget.

The scoring formula is a research variable and must be validated experimentally rather than treated as universally correct.
