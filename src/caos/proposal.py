"""Transparent user-facing cost and execution proposals."""

from dataclasses import dataclass

from .blueprint import ProductBlueprint
from .cost_optimizer import CostOption


@dataclass(frozen=True)
class BuildProposal:
    title: str
    recommendation: str
    estimated_cost: float
    estimated_time_minutes: int
    selected_resource: str
    alternatives: tuple[str, ...]
    rationale: tuple[str, ...]
    diy_steps: tuple[str, ...]


class ProposalEngine:
    """Create the two product paths: CAOS builds or user builds."""

    def create(
        self,
        blueprint: ProductBlueprint,
        selected: CostOption,
        alternatives: list[CostOption] | None = None,
    ) -> BuildProposal:
        alternatives = alternatives or []
        layer_names = [layer.name for layer in blueprint.layers]
        diy_steps = tuple(
            f"Implement and verify the {layer.lower()} layer." for layer in layer_names
        )
        rationale = (
            "Free-first policy selected a legitimate free resource when it meets the task threshold."
            if selected.is_free
            else "The free-first policy retained a paid option because it was the best feasible option under the stated constraints.",
            f"Selected resource: {selected.agent_name}.",
            f"Estimated direct execution cost: ${selected.estimated_cost:.4f}.",
        )
        return BuildProposal(
            title="CAOS Cost-Optimized Build Proposal",
            recommendation="Let CAOS Build It",
            estimated_cost=selected.estimated_cost,
            estimated_time_minutes=max(5, len(blueprint.layers) * 10),
            selected_resource=selected.agent_name,
            alternatives=tuple(option.agent_name for option in alternatives),
            rationale=rationale,
            diy_steps=diy_steps,
        )
