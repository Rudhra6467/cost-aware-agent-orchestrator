from caos.cost_router import CostAwareRouter
from caos.cost_optimizer import CostPolicy
from caos.models import AgentProfile, Task
from caos.task_router import TaskRouter


def test_only_ready_tasks_are_routed():
    tasks = [
        Task("a", "build schema"),
        Task("b", "build api", dependencies=("a",)),
        Task("c", "build ui", dependencies=("b",)),
    ]
    agents = [AgentProfile("free", "Free", coding_score=1.0)]
    routes = TaskRouter(CostAwareRouter()).route_ready_tasks(
        tasks, {"a"}, agents, policy=CostPolicy(prefer_free=True)
    )
    assert [r.task_id for r in routes] == ["b"]
    assert routes[0].decision.agent_id == "free"
