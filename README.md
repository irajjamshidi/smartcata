# PromptForge SDK

PromptForge is a local, deterministic compiler from human intent to a validated engineering task and Codex-compatible handoff. It uses only local files and deterministic rules; no network or LLM API is called.

## Quick start

```bash
python -m pytest
PYTHONPATH=src python -m promptforge.cli.main compile --input examples/vanilla-product-mvp.md --target codex
PYTHONPATH=src python -m promptforge.cli.main inspect .
```

The project declares Pydantic for packaging compatibility. The local core deliberately uses a dataclass representation so the repository can execute in minimal/offline Python environments where dependencies are absent.

## Product MVP

`mvp/` is a modular-monolith product catalog with SQLite services, CSV import/export, pricing, and a vanilla frontend. To serve the FastAPI application after installing optional dependencies:

```bash
pip install -e '.[mvp]'
uvicorn mvp.backend.main:app --reload
```

Excel endpoints explicitly return `501`: CSV is the implemented MVP import/export format.
