from promptforge.core.parser import parse
from promptforge.core.optimizer import optimize
from promptforge.core.validator import validate
from promptforge.context.ranking import rank_files
def test_task_ir_round_trip_and_rendering():
    task=optimize(parse('Build catalog with FastAPI. Use SQLite. Do not use React.'))
    assert task.objective and task.from_json(task.to_json()).title == task.title
    assert 'OBJECTIVE' in task.to_markdown()
def test_detects_frontend_conflict():
    task=parse('Build app with React and vanilla JavaScript.')
    assert any(f.code=='technology_conflict' for f in validate(task).findings)
def test_ranking_prefers_relevant_file(): assert rank_files(['x.py','pricing.py'], 'pricing')[0]=='pricing.py'
