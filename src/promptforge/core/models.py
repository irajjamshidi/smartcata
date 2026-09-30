from __future__ import annotations
import json
from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class TaskIR:
    """Versioned, serializable intermediate representation of an engineering task."""
    task_id: str = "pf-001"
    title: str = "Untitled task"
    objective: str = ""
    context: list[str] = field(default_factory=list)
    requirements: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)
    environment: dict[str, Any] = field(default_factory=dict)
    architecture: str = ""
    deliverables: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    priority: str = "medium"
    risks: list[str] = field(default_factory=list)
    execution_mode: str = "implementation"
    version: str = "1.0"

    def validate(self) -> list[str]:
        errors = []
        if not self.task_id.strip(): errors.append("task_id is required")
        if not self.title.strip(): errors.append("title is required")
        if not self.objective.strip(): errors.append("objective is required")
        return errors

    def model_dump(self) -> dict[str, Any]: return asdict(self)
    def model_dump_json(self, **kwargs: Any) -> str: return json.dumps(asdict(self), ensure_ascii=False, indent=2, **kwargs)
    def to_json(self) -> str: return self.model_dump_json()
    @classmethod
    def model_validate(cls, data: dict[str, Any]) -> "TaskIR": return cls(**data)
    @classmethod
    def from_json(cls, payload: str) -> "TaskIR": return cls.model_validate(json.loads(payload))
    def to_markdown(self) -> str:
        from promptforge.handoff.markdown import render_task
        return render_task(self)
