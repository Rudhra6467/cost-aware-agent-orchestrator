from caos.blueprint import ProductBlueprint
from caos.project_dag import ProjectDagBuilder, detect_signals


def test_signals_detect_ai_payments_and_auth():
    signals = detect_signals("Build a SaaS app with user login, AI chat and Stripe subscriptions")
    assert signals.ai
    assert signals.authentication
    assert signals.payments


def test_project_dag_adds_only_relevant_capabilities():
    graph = ProjectDagBuilder().build(ProductBlueprint("Build a simple portfolio website", [], [], [], [], [], []))
    ids = {task.task_id for task in graph.tasks}
    assert "frontend" in ids
    assert "ai" not in ids
    assert "billing" not in ids


def test_project_dag_builds_dependencies_for_ai_product():
    graph = ProjectDagBuilder().build(ProductBlueprint("Build an AI app with user accounts and saved history", [], [], [], [], [], []))
    by_id = {task.task_id: task for task in graph.tasks}
    assert "ai" in by_id
    assert "data" in by_id
    assert "auth" in by_id
    assert "data" in by_id["ai"].dependencies
    assert "frontend" in by_id["integration"].dependencies
