"""Bootstrap helpers for constructing a usable CAOS execution runtime."""

from pathlib import Path

from .agent_catalog import AgentCapability
from .agent_catalog import AgentCatalog
from .execution_engine import AgentRegistry
from .deterministic_agent import DeterministicAgent
from .execution_runtime import ExecutionRuntime
from .execution_session import ExecutionSession, ExecutionSessionManager
from .planning_contract import PlanSummary, PlanningResponse
from .task_graph import TaskGraphBuilder


def create_runtime(response: PlanningResponse, plan_id: str, workspace: str | Path) -> tuple[ExecutionRuntime, ExecutionSession]:
    """Build a complete local runtime and session from an approved plan."""
    plan = next((item for item in response.plans if item.plan_id == plan_id), None)
    if plan is None:
        raise ValueError(f"Unknown plan: {plan_id}")

    graph = TaskGraphBuilder().build(response, plan)
    sessions = ExecutionSessionManager()
    session = sessions.create(response.idea, plan, graph.as_session_tasks())

    agent = DeterministicAgent(workspace)
    roles = frozenset(node.role for node in graph.nodes.values())
    capabilities = frozenset({"general"})
    catalog = AgentCatalog([
        AgentCapability(
            agent.name,
            roles,
            capabilities,
            cost=0.0,
            quality=0.75,
            latency=0.1,
            reliability=1.0,
        )
    ])
    registry = AgentRegistry([agent])
    runtime = ExecutionRuntime(sessions, graph, catalog, registry)
    return runtime, session


def requirements_for(graph) -> dict[str, object]:
    """Create baseline requirements for every task in a graph."""
    from .agent_catalog import TaskRequirements

    return {
        task_id: TaskRequirements(node.role, frozenset({"general"}))
        for task_id, node in graph.nodes.items()
    }
