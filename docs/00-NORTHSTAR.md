# 00 — North Star

## Mission

Build an autonomous software-development orchestration system that can transform a user's software idea into a functioning, tested application by dynamically selecting and coordinating AI agents according to capability, availability, reliability, context requirements, and cost.

## The Core Question

> What is the cheapest reliable way to complete the next software-development task?

The system should answer that question continuously rather than selecting one model/provider at the beginning and blindly using it throughout execution.

## North Star Outcome

A user provides a software requirement and a budget. CAOS decomposes the requirement, evaluates available agents, selects the best economically viable agent for each task, preserves project state across handoffs, verifies results, recovers from failures, and produces a working software artifact.

## North Star Metric

**Quality-adjusted cost efficiency:** software-development task success and quality achieved per unit of AI/infrastructure cost.

## Long-Term Vision

CAOS evolves from a cost-aware agent router into an autonomous AI software-development operating system capable of planning, researching, architecting, coding, testing, reviewing, recovering, and eventually deploying software with controlled human oversight.

## What CAOS Is Not

- Not merely an n8n workflow.
- Not a chatbot with multiple prompts.
- Not a static list of AI providers.
- Not an automatic free-tier scraper.
- Not an unrestricted autonomous production deployer in early versions.

## Strategic Constraint

Budget is a design constraint and a research variable. Paid services should only be introduced when experiments demonstrate that their additional capability produces measurable value relative to cost.
