from __future__ import annotations
import re
from .models import TaskIR
TECHNOLOGIES = {"fastapi":"FastAPI", "sqlite":"SQLite", "react":"React", "vanilla javascript":"Vanilla JavaScript", "javascript":"JavaScript", "python":"Python", "csv":"CSV", "excel":"Excel", "xlsx":"Excel"}

def parse(text: str, task_id: str = "pf-001") -> TaskIR:
    sentences = [s.strip(" -\t") for s in re.split(r"[\n.!?]+", text) if s.strip()]
    objective = sentences[0] if sentences else ""
    requirements, constraints, non_goals, technologies = [], [], [], []
    for sentence in sentences:
        low = sentence.casefold()
        if re.search(r"\b(do not|don't|without|avoid|must not)\b", low):
            item = re.sub(r"^(do not|don't|without|avoid|must not)\s+", "", sentence, flags=re.I)
            non_goals.append(item)
            constraints.append(sentence)
        elif sentence != objective or "build" in low or "create" in low or "implement" in low:
            for key, name in TECHNOLOGIES.items():
                if key in low and name not in technologies: technologies.append(name)
            requirements.append(sentence)
    title = objective[:80] or "Untitled task"
    return TaskIR(task_id=task_id, title=title, objective=objective, requirements=requirements, constraints=constraints, non_goals=non_goals, environment={"technologies": technologies})
