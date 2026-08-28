"""Product blueprint contract used by project-aware DAG generation."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProductBlueprint:
    raw_idea: str
    layers: list = field(default_factory=list)
    constraints: list = field(default_factory=list)
    assumptions: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    integrations: list = field(default_factory=list)
    notes: list = field(default_factory=list)
