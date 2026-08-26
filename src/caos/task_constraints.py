"""Explicit task quality/capability constraints for cost optimization."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskConstraints:
    required_capability: str
    min_quality: float = 0.0
    min_reliability: float = 0.0
    max_unit_cost: float | None = None
    security_level: str = "standard"
    acceptance_criteria: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.required_capability:
            raise ValueError("required_capability is required")
        if not 0.0 <= self.min_quality <= 1.0:
            raise ValueError("min_quality must be between 0 and 1")
        if not 0.0 <= self.min_reliability <= 1.0:
            raise ValueError("min_reliability must be between 0 and 1")
        if self.max_unit_cost is not None and self.max_unit_cost < 0:
            raise ValueError("max_unit_cost cannot be negative")
        if self.security_level not in {"standard", "high", "critical"}:
            raise ValueError("security_level must be standard, high, or critical")


@dataclass(frozen=True)
class ResourceQuality:
    quality: float
    reliability: float
    security_level: str = "standard"

    def __post_init__(self) -> None:
        if not 0.0 <= self.quality <= 1.0 or not 0.0 <= self.reliability <= 1.0:
            raise ValueError("quality and reliability must be between 0 and 1")
        if self.security_level not in {"standard", "high", "critical"}:
            raise ValueError("security_level must be standard, high, or critical")


def satisfies_constraints(constraints: TaskConstraints, cost: float, quality: ResourceQuality) -> bool:
    security_rank = {"standard": 0, "high": 1, "critical": 2}
    if cost < 0 or quality.quality < constraints.min_quality or quality.reliability < constraints.min_reliability:
        return False
    if constraints.max_unit_cost is not None and cost > constraints.max_unit_cost:
        return False
    return security_rank[quality.security_level] >= security_rank[constraints.security_level]
