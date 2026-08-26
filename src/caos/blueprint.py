"""Phase 1: turn a plain-language product idea into a reviewable blueprint."""

from dataclasses import dataclass
from enum import Enum


class BlueprintStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    NEEDS_CLARIFICATION = "needs_clarification"
    REJECTED = "rejected"


@dataclass(frozen=True)
class BlueprintLayer:
    name: str
    purpose: str
    components: tuple[str, ...]


@dataclass(frozen=True)
class ProductBlueprint:
    raw_idea: str
    summary: str
    layers: tuple[BlueprintLayer, ...]
    assumptions: tuple[str, ...] = ()
    open_questions: tuple[str, ...] = ()
    status: BlueprintStatus = BlueprintStatus.DRAFT

    @property
    def ready_for_cost_planning(self) -> bool:
        return self.status == BlueprintStatus.APPROVED and not self.open_questions


class BlueprintEngine:
    """Deterministic baseline; later backed by an LLM/research agent."""

    def analyze(self, raw_idea: str) -> ProductBlueprint:
        idea = raw_idea.strip()
        if not idea:
            raise ValueError("Idea cannot be empty.")

        lower = idea.lower()
        frontend = ["User interface", "Navigation", "Responsive experience"]
        backend = ["Application logic", "API/service layer"]
        data = ["User/project data", "Persistence and data validation"]
        infrastructure = ["Hosting/deployment", "Environment configuration"]
        external = []
        questions: list[str] = []

        if any(term in lower for term in ("ai", "assistant", "recommend", "generate", "chat")):
            external.append("AI/model service")
        if any(term in lower for term in ("payment", "subscription", "checkout")):
            external.append("Payment provider")
        if any(term in lower for term in ("notification", "sms", "email")):
            external.append("Notification provider")
        if not external:
            external.append("Third-party services only if required")

        assumptions = (
            "Initial scope targets a functional MVP rather than every future feature.",
            "Security, privacy, testing and deployment are part of the implementation plan.",
        )

        layers = (
            BlueprintLayer("Frontend", "How users see and interact with the product.", tuple(frontend)),
            BlueprintLayer("Backend", "Business logic, APIs and application services.", tuple(backend)),
            BlueprintLayer("Database", "Persistent application data and state.", tuple(data)),
            BlueprintLayer("Infrastructure", "Hosting, configuration and deployment.", tuple(infrastructure)),
            BlueprintLayer("External Resources", "Third-party or AI capabilities required by the product.", tuple(external)),
        )

        if len(idea) < 25:
            questions.append("What is the primary user outcome the first version must deliver?")

        return ProductBlueprint(
            raw_idea=idea,
            summary=f"Build a functional MVP for: {idea}",
            layers=layers,
            assumptions=assumptions,
            open_questions=tuple(questions),
        )

    def apply_user_decision(self, blueprint: ProductBlueprint, decision: str) -> ProductBlueprint:
        normalized = decision.strip().lower()
        if normalized in {"approve", "approved", "looks good", "1"}:
            if blueprint.open_questions:
                return ProductBlueprint(**{**blueprint.__dict__, "status": BlueprintStatus.NEEDS_CLARIFICATION})
            return ProductBlueprint(**{**blueprint.__dict__, "status": BlueprintStatus.APPROVED})
        if normalized in {"clarify", "specs", "2", "looks ok"}:
            return ProductBlueprint(**{**blueprint.__dict__, "status": BlueprintStatus.NEEDS_CLARIFICATION})
        if normalized in {"refine", "reject", "3", "not good"}:
            return ProductBlueprint(**{**blueprint.__dict__, "status": BlueprintStatus.REJECTED})
        raise ValueError("Decision must be approve, clarify, or refine/reject.")
