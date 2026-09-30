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
def test_variants_are_persisted_and_deleted_with_product(tmp_path):
 db = connect(tmp_path / 'variants.db')
 product = crud.create(db, {'sku': 'LED-1', 'name': 'LED Strip', 'attributes': {'color': 'white'}, 'variants': [{'sku': 'LED-WARM', 'name': 'Warm', 'attributes': {'kelvin': 3000}, 'price': 120}]})
 assert product['attributes'] == {'color': 'white'}
 assert product['variants'][0]['attributes'] == {'kelvin': 3000}
 assert crud.delete(db, product['id'])
 assert db.execute('SELECT count(*) FROM variants').fetchone()[0] == 0
def test_malformed_attributes_are_rejected_before_writing(tmp_path):
 db = connect(tmp_path / 'attributes.db')
 try:
  crud.create(db, {'sku': 'BAD-1', 'name': 'Bad attributes', 'attributes': 'not json'})
 except ValueError as error:
  assert str(error) == 'attributes must be a JSON object'
 else:
  raise AssertionError('malformed attributes should be rejected')
 assert crud.list_products(db)['total'] == 0
def test_json_attributes_are_normalized_and_validated_for_variants(tmp_path):
 db = connect(tmp_path / 'variant-attributes.db')
 product = crud.create(db, {'sku': 'GOOD-1', 'name': 'Good attributes', 'attributes': '{"color":"white"}'})
 assert product['attributes'] == {'color': 'white'}
 try:
  crud.update(db, product['id'], {'variants': [{'name': 'Broken', 'attributes': 'not json'}]})
 except ValueError as error:
  assert str(error) == 'attributes must be a JSON object'
 else:
  raise AssertionError('malformed variant attributes should be rejected')
 assert crud.get(db, product['id'])['variants'] == []
def test_variant_payloads_must_be_objects(tmp_path):
 db = connect(tmp_path / 'variant-payload.db')
 try:
  crud.create(db, {'sku': 'BAD-VARIANT', 'name': 'Bad variant', 'variants': ['not an object']})
 except ValueError as error:
  assert str(error) == 'each variant must be an object'
 else:
  raise AssertionError('non-object variants should be rejected')
 assert crud.list_products(db)['total'] == 0
def test_database_initializes_reference_tables(tmp_path):
 db = connect(tmp_path / 'reference.db')
 db.execute("INSERT INTO categories(name) VALUES ('Lighting')")
 db.execute("INSERT INTO brands(name) VALUES ('Acme')")
 db.commit()
 assert db.execute('SELECT name FROM categories').fetchone()[0] == 'Lighting'
 assert db.execute('SELECT name FROM brands').fetchone()[0] == 'Acme'
