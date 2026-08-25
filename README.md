# CAOS — Cost-Aware Orchestration System

**Working title:** Autonomous Cost-Aware Multi-Agent Software Development Framework

> **Build your idea for the lowest practical cost.**

CAOS is a research-oriented Meta-Agent orchestration system designed to help budget-constrained developers turn software ideas into functioning, tested software—or receive a detailed roadmap to build it themselves.

CAOS researches the implementation ecosystem, decomposes ideas into tasks, evaluates legitimate free/open-source/trial/discounted/low-cost/paid resources, and selects an economically practical execution strategy.

## Product Paths

### 1. Let CAOS Build It

CAOS researches, plans, executes, verifies, and recovers from failures to deliver a working software artifact within user-defined constraints.

### 2. Show Me How

CAOS provides a detailed, cost-optimized DIY roadmap covering architecture, tools, setup, implementation sequence, expected costs, alternatives, and verification.

## Legitimate Cost Minimization

CAOS optimizes for the **lowest practical cost**, not reckless zero-cost behavior. It may use legitimate free tiers, open-source/local models, published trials and discounts, low-cost APIs, and paid resources where their incremental value justifies the cost.

CAOS must not circumvent rate limits, payment controls, trial restrictions, identity requirements, or provider terms.

## North Star

Transform a user's idea into a verified software outcome using the lowest practical total cost while satisfying functionality, quality, reliability, security, time, and budget constraints.

## Primary Research Question

> Can cost-aware task-level resource selection achieve comparable or better software outcomes at materially lower cost than fixed-provider or strongest-model baselines?

## Current Status

**M1 — First Agent Foundation: In progress**

The repository contains the project constitution, product specification, architecture, resource intelligence specification, cost optimizer specification, research plan, experiment framework, progress tracker, and an executable Python orchestration foundation with tests and CI.

## Initial Technical Direction

- Decision/orchestration logic: Python
- Visual/operational integration: n8n where useful
- Project artifact state: Git/GitHub
- Structured orchestration state: SQLite initially
- Verification: automated build/test/lint pipeline
- Provider-neutral agent adapters
- Initial roles: Researcher, Planner, Architect, Developer, Reviewer, Tester, Cost Optimizer

## Development Sequence

Foundation → Single-Agent Builder → Resource Registry → Real LLM Execution → Persistent State → Context Handoff → Multi-Agent → Dynamic Resource Selection → Failure Recovery → Verification → Cost Optimization → Benchmarking → CAOS Alpha.

See `docs/` for the permanent project source of truth.
