from .scanner import inspect_project
from .ranking import rank_files
def build_context(path, task_text):
    context=inspect_project(path); context['relevant_files']=rank_files(context['files'], task_text)[:20]; context.pop('files', None); return context
