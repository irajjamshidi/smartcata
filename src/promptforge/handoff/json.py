from promptforge.core.models import TaskIR
def render_json(task: TaskIR) -> str: return task.to_json()
