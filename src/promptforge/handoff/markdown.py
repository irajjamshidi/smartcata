from promptforge.core.models import TaskIR
from promptforge.core.planner import plan
CONTRACT = ["Inspect the existing project first.", "Do not rewrite working code unnecessarily.", "Respect the existing architecture.", "Implement the smallest correct solution and avoid unnecessary dependencies.", "Run tests, fix failures, and verify acceptance criteria.", "Report changed files, tests executed, and unresolved issues.", "Do not claim success without verification."]
def _section(title, values):
    values = values if isinstance(values, list) else [values]
    return f"## {title}\n" + ("\n".join(f"- {v}" for v in values if v) or "- None") + "\n"
def render_task(task: TaskIR) -> str:
    sections=[f"# {task.title}\n", _section("OBJECTIVE", task.objective), _section("PROJECT CONTEXT", task.context), _section("REQUIREMENTS", task.requirements), _section("CONSTRAINTS", task.constraints), _section("NON-GOALS", task.non_goals), _section("ASSUMPTIONS", task.assumptions), _section("OPEN QUESTIONS", task.open_questions), _section("ARCHITECTURE", task.architecture), _section("IMPLEMENTATION PLAN", [f"Phase {p['phase']}: {p['name']}" for p in plan(task)]), _section("DELIVERABLES", task.deliverables), _section("ACCEPTANCE CRITERIA", task.acceptance_criteria), _section("TEST REQUIREMENTS", task.tests), _section("RISKS", task.risks), _section("EXECUTION INSTRUCTIONS", CONTRACT)]
    return "\n".join(sections)
