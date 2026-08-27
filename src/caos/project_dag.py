"""Project-aware task DAG generation from a validated product blueprint."""

from dataclasses import dataclass

from .blueprint import ProductBlueprint
from .models import Task
from .dag import AcceptanceCriterion, TaskGraph


@dataclass(frozen=True)
class ProjectSignals:
    """Normalized capability signals extracted from an idea."""
    frontend: bool
    backend: bool
    database: bool
    authentication: bool
    ai: bool
    payments: bool
    notifications: bool


def detect_signals(idea: str) -> ProjectSignals:
    text = idea.lower()
    return ProjectSignals(
        frontend=True,
        backend=any(x in text for x in ("app", "api", "saas", "platform", "website", "backend")),
        database=any(x in text for x in ("track", "history", "profile", "account", "save", "database", "users")),
        authentication=any(x in text for x in ("login", "sign in", "account", "authentication", "user")),
        ai=any(x in text for x in ("ai", "artificial intelligence", "chatbot", "recommend", "recommendation", "llm", "assistant")),
        payments=any(x in text for x in ("payment", "pay", "stripe", "subscription", "billing", "checkout")),
        notifications=any(x in text for x in ("notification", "email", "sms", "push", "alert")),
    )


class ProjectDagBuilder:
    """Create a deterministic project-specific baseline DAG.

    This is a rules-based baseline, not an LLM. Its purpose is to provide a
    safe, inspectable graph that later agents may enrich but must validate.
    """

    def build(self, blueprint: ProductBlueprint) -> TaskGraph:
        signals = detect_signals(blueprint.raw_idea)
        tasks: list[Task] = [
            Task("req", "Finalize product requirements and acceptance criteria", "architecture", 700, 1000, 5.0),
        ]
        if signals.database:
            tasks.append(Task("data", "Design data model and persistence", "database", 900, 1400, 5.0, dependencies=("req",)))
        if signals.authentication:
            deps = ("data",) if signals.database else ("req",)
            tasks.append(Task("auth", "Implement authentication and authorization", "coding", 1200, 2200, 6.0, dependencies=deps))
        if signals.ai:
            deps = ("data",) if signals.database else ("req",)
            tasks.append(Task("ai", "Integrate AI capability and define model/tool boundaries", "ai", 1200, 2200, 6.0, dependencies=deps))
        if signals.payments:
            deps = ("data",) if signals.database else ("req",)
            tasks.append(Task("billing", "Implement payment, billing and webhook flows", "coding", 1300, 2300, 6.0, dependencies=deps))
        if signals.notifications:
            deps = ("data",) if signals.database else ("req",)
            tasks.append(Task("notify", "Implement notification delivery and preferences", "coding", 900, 1600, 6.0, dependencies=deps))

        frontend_deps = ["req"]
        if signals.authentication: frontend_deps.append("auth")
        tasks.append(Task("frontend", "Build primary frontend user flows", "coding", 1400, 2600, 6.0, dependencies=tuple(frontend_deps)))

        integration_deps = ["frontend"]
        for task_id in ("data", "ai", "billing", "notify"):
            if any(t.task_id == task_id for t in tasks): integration_deps.append(task_id)
        tasks.extend([
            Task("integration", "Integrate application components and external services", "coding", 1200, 2200, 6.0, dependencies=tuple(integration_deps)),
            Task("verify", "Run automated verification and repair verified failures", "coding", 1300, 2300, 6.0, dependencies=("integration",)),
            Task("release", "Verify acceptance criteria and prepare deployment", "architecture", 900, 1300, 5.0, dependencies=("verify",)),
        ])

        criteria = tuple(AcceptanceCriterion(f"AC-{task.task_id}", task.description, task.task_id) for task in tasks)
        graph = TaskGraph(tuple(tasks), criteria)
        graph.validate()
        return graph
