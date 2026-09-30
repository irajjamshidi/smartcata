"""PromptForge: deterministic task compilation for coding agents."""
from .version import __version__
from .core.models import TaskIR
__all__ = ["TaskIR", "__version__"]
