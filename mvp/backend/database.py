"""SQLite initialization for the Product Intelligence MVP."""
import sqlite3
from pathlib import Path

SCHEMA = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    slug TEXT,
    brand TEXT,
    category TEXT,
    model TEXT,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    image TEXT,
    attributes TEXT NOT NULL DEFAULT '{}',
    cost REAL NOT NULL DEFAULT 0,
    price REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'IRT' CHECK(currency IN ('IRT', 'IRR', 'USD', 'EUR')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS variants (
    variant_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku TEXT UNIQUE,
    name TEXT NOT NULL,
    attributes TEXT NOT NULL DEFAULT '{}',
    price REAL,
    status TEXT NOT NULL DEFAULT 'active'
);
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
'''

def connect(path: str | Path = 'mvp/data/app.db') -> sqlite3.Connection:
    """Open an initialized connection with foreign keys enabled."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    database = sqlite3.connect(path)
    database.row_factory = sqlite3.Row
    database.execute('PRAGMA foreign_keys = ON')
    database.executescript(SCHEMA)
    database.commit()
    return database
