"""Minimal CLI demonstration for the CAOS planning experience."""

from __future__ import annotations

import argparse

from .cost_optimizer import CostPolicy
from .models import AgentProfile
from .pipeline import CostAwarePipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="CAOS cost-aware project planner")
    parser.add_argument("idea", help="plain-language product idea")
    parser.add_argument("--budget", type=float, default=None)
    args = parser.parse_args()

    agents = [
        AgentProfile("free-coder", "Free Coder", coding_score=0.70, architecture_score=0.55),
        AgentProfile(
            "premium-coder",
            "Premium Coder",
            coding_score=0.95,
            architecture_score=0.95,
            cost_per_1k_input=0.01,
            cost_per_1k_output=0.02,
        ),
    ]
    plan = CostAwarePipeline(agents).create_plan(
        args.idea,
        CostPolicy(budget_remaining=args.budget),
    )

    print("CAOS COST-OPTIMIZED BUILD PLAN")
    print("================================")
    print(f"Idea: {plan.blueprint.raw_idea}")
    print(f"Tasks: {len(plan.tasks)}")
    print(f"Estimated first-task cost: ${plan.proposal.estimated_cost:.4f}")
    print(f"Recommended resource: {plan.proposal.selected_resource}")
    print("\nTask routing:")
    for item in plan.tasks:
        print(f"- {item.task.task_id}: {item.recommended.agent_name} (${item.recommended.estimated_cost:.4f})")
    print("\nDIY path:")
    for step in plan.proposal.diy_steps:
        print(f"- {step}")


if __name__ == "__main__":
    main()
