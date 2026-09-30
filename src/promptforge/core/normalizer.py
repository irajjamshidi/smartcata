from .models import TaskIR
ALIASES = {"vanilla js":"Vanilla JavaScript", "js":"JavaScript", "fast api":"FastAPI", "sqlite3":"SQLite"}
def _unique(items):
    seen=set(); out=[]
    for item in items:
        value=" ".join(str(item).split()).strip()
        key=value.casefold()
        if value and key not in seen: seen.add(key); out.append(value)
    return out
def normalize(task: TaskIR) -> TaskIR:
    for name in ("context", "requirements", "constraints", "assumptions", "open_questions", "non_goals", "deliverables", "acceptance_criteria", "tests", "risks"):
        setattr(task, name, _unique(getattr(task, name)))
    techs = task.environment.get("technologies", [])
    task.environment["technologies"] = _unique([ALIASES.get(str(t).casefold(), t) for t in techs])
    return task
