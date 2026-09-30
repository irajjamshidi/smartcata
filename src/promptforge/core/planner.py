from .models import TaskIR
def plan(task: TaskIR) -> list[dict[str, str]]:
    return [{"phase":"1", "name":"Inspect project", "depends_on":""}, {"phase":"2", "name":"Confirm architecture", "depends_on":"1"}, {"phase":"3", "name":"Implement smallest solution", "depends_on":"2"}, {"phase":"4", "name":"Run tests and verify acceptance criteria", "depends_on":"3"}]
