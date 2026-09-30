# Test report

Run `python -m pytest` from the repository root. The suite validates PromptForge serialization/rendering, conflict detection, relevance ranking, and the product SQLite CRUD/search/import/duplicate/export/pricing flow. FastAPI serving is dependency-gated and was not executed in the minimal offline environment unless optional extras are installed.
