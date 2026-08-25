# 06 — Research Plan

## Primary Research Focus

**Cost-Aware Dynamic Agent Selection** with context-preserving handoff as a supporting research component.

## Primary Research Question

Can dynamic selection of AI agents based on task capability, cost, availability, reliability, and context fit reduce total execution cost while maintaining acceptable software-development quality and task-success rates?

## Hypothesis

A dynamic cost-aware orchestration strategy can achieve comparable or acceptable software-development outcomes at lower total AI cost than a fixed-agent strategy, particularly when agents have heterogeneous capability, pricing, latency, and availability.

## Baselines

1. Single-agent baseline using one capable model.
2. Fixed multi-agent baseline with predetermined roles/providers.
3. Cheapest-available baseline.
4. CAOS dynamic-selection strategy.

## Primary Metrics

- Task success rate
- Automated test pass rate
- Code quality/review score
- Total AI cost
- Input/output tokens
- Execution time
- Number of retries
- Number of handoffs
- Failure recovery rate
- Context retention

## Context Handoff Experiment

Compare:

A. Full conversation passed between agents.

B. Free-form summary passed between agents.

C. Structured project-state handoff passed between agents.

D. Structured state + Git project state.

Measure requirement retention, architecture retention, implementation continuity, test success, and context size.

## Research Discipline

Every experiment should record its configuration, task set, agent versions, budget, execution traces, metrics, outcome, and conclusion. Results must not be generalized beyond the tested conditions without evidence.
