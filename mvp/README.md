# Product Intelligence MVP

A lightweight FastAPI + SQLite + vanilla JavaScript product core. Implemented API endpoints include product CRUD, category/brand listing, CSV import, catalog, and CSV export. The UI provides API-backed search and product creation.

Run with `pip install -e '.[mvp]' && uvicorn mvp.backend.main:app --reload`. CSV columns: `sku,name,brand,category,cost,price,currency`.
