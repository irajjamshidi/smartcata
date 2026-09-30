from .models import TaskIR
from .normalizer import normalize
from .validator import validate
def optimize(task: TaskIR) -> TaskIR:
    task=normalize(task)
    if not task.acceptance_criteria:
        task.acceptance_criteria=[f"Verify: {r}" for r in task.requirements[:5]]
    if not task.tests:
        task.tests=[f"Automated or manual verification for: {r}" for r in task.requirements[:5]]
    for finding in validate(task).findings:
        if finding.code == "ambiguity" and finding.message not in task.open_questions: task.open_questions.append(finding.message)
        if finding.code == "scope_creep" and finding.message not in task.risks: task.risks.append(finding.message)
    return task
