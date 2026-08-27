"""Explicit user constraints for CAOS planning."""

from dataclasses import dataclass
from enum import Enum


class Autonomy(str, Enum):
    CONTROLLED = "controlled"
    AUTONOMOUS = "autonomous"
    DIY = "diy"


@dataclass(frozen=True)
class UserConstraints:
    budget: float = 0.0
    quality_threshold: float = 0.7
    max_build_days: float | None = None
    autonomy: Autonomy = Autonomy.CONTROLLED
    prefer_free: bool = True

    def __post_init__(self) -> None:
        if self.budget < 0:
            raise ValueError("Budget cannot be negative")
        if not 0 <= self.quality_threshold <= 1:
            raise ValueError("Quality threshold must be between 0 and 1")
        if self.max_build_days is not None and self.max_build_days <= 0:
            raise ValueError("Maximum build time must be positive")
