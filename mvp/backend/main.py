"""FastAPI application for the Product Intelligence MVP.

Run with: ``uvicorn mvp.backend.main:app --reload`` after installing ``.[mvp]``.
"""
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from mvp.backend import crud
from mvp.backend.database import connect
from mvp.backend.services.exporters import export_csv
from mvp.backend.services.importers import import_csv

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / 'frontend'
app = FastAPI(title='Product Intelligence MVP')
app.mount('/static', StaticFiles(directory=FRONTEND), name='static')

def db():
    return connect()

def _product_or_404(product_id: int):
    product = crud.get(db(), product_id)
    if product is None:
        raise HTTPException(404, 'Product not found')
    return product

@app.get('/api/products')
def products(search: str = '', brand: str = '', category: str = '', status: str = '', page: int = 1):
    return crud.list_products(db(), search, brand, category, status, max(1, page))

@app.get('/api/products/{product_id}')
def product(product_id: int):
    return _product_or_404(product_id)

@app.post('/api/products', status_code=201)
def create(data: dict):
    try:
        return crud.create(db(), data)
    except (ValueError, sqlite3.IntegrityError) as error:
        # sqlite integrity failures and required-field errors are client input errors.
        raise HTTPException(422, str(error)) from error

@app.put('/api/products/{product_id}')
def update(product_id: int, data: dict):
    try:
        item = crud.update(db(), product_id, data)
    except (ValueError, sqlite3.IntegrityError) as error:
        raise HTTPException(422, str(error)) from error
    if item is None:
        raise HTTPException(404, 'Product not found')
    return item

@app.delete('/api/products/{product_id}')
def remove(product_id: int):
    if not crud.delete(db(), product_id):
        raise HTTPException(404, 'Product not found')
    return {'deleted': True}

@app.get('/api/categories')
def categories():
    return [row[0] for row in db().execute("SELECT name FROM categories UNION SELECT DISTINCT category FROM products WHERE category != '' ORDER BY 1").fetchall()]

@app.post('/api/categories', status_code=201)
def category(data: dict):
    name = str(data.get('name', '')).strip()
    if not name:
        raise HTTPException(422, 'category name is required')
    database = db()
    database.execute('INSERT OR IGNORE INTO categories(name) VALUES (?)', (name,))
    database.commit()
    return {'name': name}

@app.get('/api/brands')
def brands():
    return [row[0] for row in db().execute("SELECT name FROM brands UNION SELECT DISTINCT brand FROM products WHERE brand != '' ORDER BY 1").fetchall()]

@app.post('/api/brands', status_code=201)
def brand(data: dict):
    name = str(data.get('name', '')).strip()
    if not name:
        raise HTTPException(422, 'brand name is required')
    database = db()
    database.execute('INSERT OR IGNORE INTO brands(name) VALUES (?)', (name,))
    database.commit()
    return {'name': name}

@app.post('/api/import/csv')
async def upload_csv(file: UploadFile):
    return import_csv(db(), await file.read())

@app.post('/api/import/excel')
async def upload_excel(file: UploadFile):
    raise HTTPException(501, 'Excel import is deferred; use CSV for this MVP.')

@app.get('/api/catalog')
def catalog():
    return crud.list_products(db(), per_page=100)['items']

@app.get('/api/export/csv')
def csv_export():
    content = export_csv(crud.list_products(db(), per_page=10_000)['items'])
    return Response(content, media_type='text/csv', headers={'Content-Disposition': 'attachment; filename=products.csv'})

@app.get('/api/export/excel')
def excel_export():
    raise HTTPException(501, 'Excel export is deferred; use CSV for this MVP.')

@app.get('/')
def frontend():
    return FileResponse(FRONTEND / 'index.html')
