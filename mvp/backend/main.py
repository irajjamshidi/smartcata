"""FastAPI application. Install the optional 'mvp' dependencies to run it."""
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException, UploadFile
    from fastapi.responses import Response, FileResponse
    from fastapi.staticfiles import StaticFiles
except ImportError as error:
    raise RuntimeError("Install project extras: pip install -e '.[mvp]'") from error
from mvp.backend.database import connect
from mvp.backend import crud
from mvp.backend.services.importers import import_csv
from mvp.backend.services.exporters import export_csv
app=FastAPI(title='Product Intelligence MVP')
FRONTEND_DIR=Path(__file__).resolve().parent.parent/'frontend'
app.mount('/css', StaticFiles(directory=FRONTEND_DIR/'css'), name='css')
app.mount('/js', StaticFiles(directory=FRONTEND_DIR/'js'), name='js')
def db(): return connect()
@app.get('/api/products')
def products(search:str='',brand:str='',category:str='',status:str='',page:int=1): return crud.list_products(db(),search,brand,category,status,page)
@app.get('/api/products/{product_id}')
def product(product_id:int):
    item=crud.get(db(),product_id)
    if not item: raise HTTPException(404,'Product not found')
    return item
@app.post('/api/products')
def create(data:dict): return crud.create(db(),data)
@app.put('/api/products/{product_id}')
def update(product_id:int,data:dict):
    item=crud.update(db(),product_id,data)
    if not item: raise HTTPException(404,'Product not found')
    return item
@app.delete('/api/products/{product_id}')
def remove(product_id:int): return {'deleted':crud.delete(db(),product_id)}
@app.get('/api/categories')
def categories(): return [r[0] for r in db().execute("select distinct category from products where category != ''").fetchall()]
@app.post('/api/categories')
def category(data:dict): return data
@app.get('/api/brands')
def brands(): return [r[0] for r in db().execute("select distinct brand from products where brand != ''").fetchall()]
@app.post('/api/brands')
def brand(data:dict): return data
@app.post('/api/import/csv')
async def upload_csv(file:UploadFile): return import_csv(db(),await file.read())
@app.post('/api/import/excel')
async def upload_excel(file:UploadFile): raise HTTPException(501,'Excel import is deferred; use CSV for this MVP.')
@app.get('/api/catalog')
def catalog(): return crud.all_products(db())
@app.get('/api/export/csv')
def csv_export(): return Response(export_csv(crud.all_products(db())), media_type='text/csv', headers={'Content-Disposition':'attachment; filename=products.csv'})
@app.get('/api/export/excel')
def excel_export(): raise HTTPException(501,'Excel export is deferred; use CSV for this MVP.')
@app.get('/')
def frontend(): return FileResponse(FRONTEND_DIR/'index.html')
