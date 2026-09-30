# Architecture

PromptForge moves text through deterministic parsing, normalization, validation, planning, optimization, context inspection/ranking, and handoff rendering. `TaskIR` is the versioned JSON/Markdown boundary. The scanner records metadata and relevant paths instead of repository contents.

The Product MVP is a modular monolith: FastAPI routes call SQLite CRUD and focused import, pricing, and export services. The browser uses the REST API with vanilla ES modules.
