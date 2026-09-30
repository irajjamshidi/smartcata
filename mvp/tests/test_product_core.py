from mvp.backend.database import connect
from mvp.backend import crud
from mvp.backend.services.pricing import calculate_price
from mvp.backend.services.importers import import_csv
from mvp.backend.services.exporters import export_csv
def test_crud_search_import_and_export(tmp_path):
 db=connect(tmp_path/'app.db'); one=crud.create(db,{'sku':'P-1','name':'محصول تست','price':10}); assert crud.get(db,one['id'])['name']=='محصول تست'; assert crud.list_products(db,search='تست')['total']==1
 summary=import_csv(db,b'sku,name,price\nP-2,LED,120\nP-2,LED updated,125\n,missing,0\n'); assert summary['imported']==1 and summary['updated']==1 and summary['rejected']==1; assert 'P-2' in export_csv(crud.list_products(db,per_page=10)['items'])
def test_pricing(): assert calculate_price(100,20)==120
def test_imports_500_products(tmp_path):
 db=connect(tmp_path/'bulk.db')
 rows=['sku,name,price']+[f'SKU-{n},محصول {n},{n}' for n in range(500)]
 summary=import_csv(db, ('\n'.join(rows)).encode())
 assert summary['imported']==500 and crud.list_products(db,per_page=1)['total']==500
