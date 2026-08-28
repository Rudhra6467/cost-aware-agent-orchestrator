"""Runnable entry point for the first CAOS browser experience."""

from __future__ import annotations

from .http_api import serve
from .models import AgentProfile
from .pipeline import CostAwarePipeline


def build_demo_pipeline() -> CostAwarePipeline:
    """Create a deterministic local demo resource pool with no credentials."""
    return CostAwarePipeline([
        AgentProfile(
            agent_id="free-coder",
            name="Free Coder",
            coding_score=0.80,
            architecture_score=0.60,
            context_window=8_000,
            reliability=0.85,
            availability=0.95,
        ),
        AgentProfile(
            agent_id="premium-coder",
            name="Premium Coder",
            coding_score=0.95,
            architecture_score=0.90,
            context_window=16_000,
            cost_per_1k_input=0.001,
            cost_per_1k_output=0.002,
            reliability=0.98,
            availability=0.99,
        ),
    ])


def main() -> None:
    serve(build_demo_pipeline)


if __name__ == "__main__":
    main()
