import pytest

from caos.blueprint import ProductBlueprint
from caos.enrichment import TaskEnricher, validate_enrichment
from caos.project_dag import ProjectDagBuilder


def graph():
    return ProjectDagBuilder().build(ProductBlueprint("Build an AI app with user accounts", [], [], [], [], [], []))


def test_enrichment_covers_every_task():
    g = graph()
    enriched = TaskEnricher().enrich(g)
    assert {x.task_id for x in enriched} == {x.task_id for x in g.tasks}
    validate_enrichment(g, enriched)


def test_enrichment_has_security_and_acceptance_checks():
    item = TaskEnricher().enrich(graph())[0]
    assert item.security_requirements
    assert item.acceptance_tests
    assert item.estimated_tokens > 0


def test_validation_rejects_incomplete_enrichment():
    g = graph()
    with pytest.raises(ValueError):
        validate_enrichment(g, ())
