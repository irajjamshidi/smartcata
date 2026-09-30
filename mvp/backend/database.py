import sqlite3
from pathlib import Path
SCHEMA='''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, sku TEXT UNIQUE NOT NULL, name TEXT NOT NULL, slug TEXT, brand TEXT, category TEXT, model TEXT, description TEXT, status TEXT DEFAULT 'active', image TEXT, attributes TEXT DEFAULT '{}', cost REAL DEFAULT 0, price REAL DEFAULT 0, currency TEXT DEFAULT 'IRT', created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);'''
def connect(path='mvp/data/app.db'):
    Path(path).parent.mkdir(parents=True, exist_ok=True); db=sqlite3.connect(path); db.row_factory=sqlite3.Row; db.execute(SCHEMA); db.commit(); return db
