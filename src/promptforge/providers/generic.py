from .base import Provider
from promptforge.handoff.markdown import render_task
class GenericProvider(Provider):
    name='generic'
    def compile(self, task): return render_task(task)
class CodexProvider(GenericProvider):
    name='codex'
