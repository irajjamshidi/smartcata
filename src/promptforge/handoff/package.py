from pathlib import Path
from .markdown import render_task
from .json import render_json
def write_package(task, context, output='.codex/task'):
    directory=Path(output); directory.mkdir(parents=True, exist_ok=True)
    (directory/'task.md').write_text(render_task(task), encoding='utf-8')
    (directory/'task.json').write_text(render_json(task), encoding='utf-8')
    (directory/'context.md').write_text(context.get('markdown','No project context supplied.'), encoding='utf-8')
    (directory/'acceptance.md').write_text('\n'.join(f'- {x}' for x in task.acceptance_criteria), encoding='utf-8')
    (directory/'tests.md').write_text('\n'.join(f'- {x}' for x in task.tests), encoding='utf-8')
    return directory
