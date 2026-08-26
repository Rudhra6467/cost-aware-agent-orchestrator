"""Execution policies for moving from a proposal into a controlled build."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ControlMode(str, Enum):
    CONTROLLED = "controlled"
    AUTONOMOUS = "autonomous"


@dataclass(frozen=True)
class ExecutionPolicy:
    """Safety and autonomy constraints for a build run."""

    mode: ControlMode = ControlMode.CONTROLLED
    max_repair_attempts: int = 2
    max_task_cost: float | None = None
    require_verification: bool = True
    allow_paid_resources: bool = False

    def can_execute_paid(self, estimated_cost: float) -> bool:
        if not self.allow_paid_resources:
            return estimated_cost <= 0.0
        if self.max_task_cost is None:
            return True
        return estimated_cost <= self.max_task_cost
