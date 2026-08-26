"""User-facing decision and budget policy primitives."""

from dataclasses import dataclass
from enum import Enum


class BuildMode(str, Enum):
    CAOS_BUILD = "caos_build"
    DIY = "diy"


class ControlMode(str, Enum):
    CONTROLLED = "controlled"
    AUTONOMOUS = "autonomous"


@dataclass(frozen=True)
class UserConstraints:
    """Preferences that shape optimization without changing functionality."""

    budget: float | None = None
    cost_priority: float = 1.0
    speed_priority: float = 0.0
    quality_priority: float = 0.0
    control_mode: ControlMode = ControlMode.CONTROLLED

    def __post_init__(self) -> None:
        for name, value in (
            ("cost_priority", self.cost_priority),
            ("speed_priority", self.speed_priority),
            ("quality_priority", self.quality_priority),
        ):
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.budget is not None and self.budget < 0:
            raise ValueError("budget cannot be negative")


@dataclass(frozen=True)
class UserDecision:
    mode: BuildMode
    constraints: UserConstraints
    approved: bool

    def can_execute(self) -> bool:
        return self.approved and self.mode in {BuildMode.CAOS_BUILD, BuildMode.DIY}
