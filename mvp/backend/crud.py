"""Small SQLite repository for products and their basic variants."""
from collections.abc import Mapping
import json

ALLOWED = {'sku', 'name', 'slug', 'brand', 'category', 'model', 'description', 'status', 'image', 'attributes', 'cost', 'price', 'currency'}
VARIANT_ALLOWED = {'sku', 'name', 'attributes', 'price', 'status'}

def _encode_attributes(value):
    """Validate and serialize attributes before they reach SQLite."""
    if value in (None, ''):
        return '{}'
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError('attributes must be a JSON object') from error
    if not isinstance(value, Mapping):
        raise ValueError('attributes must be a JSON object')
    return json.dumps(value, ensure_ascii=False)


def _encode(data, allowed):
    return {
        key: _encode_attributes(value) if key == 'attributes' else value
        for key, value in data.items()
        if key in allowed
    }

def _variant_rows(db, product_id):
    rows = db.execute('SELECT variant_id, product_id, sku, name, attributes, price, status FROM variants WHERE product_id=? ORDER BY variant_id', (product_id,)).fetchall()
    return [{**dict(row), 'attributes': json.loads(row['attributes'] or '{}')} for row in rows]

def _product(row, db=None):
    if row is None:
        return None
    product = dict(row)
    product['attributes'] = json.loads(product['attributes'] or '{}')
    if db is not None:
        product['variants'] = _variant_rows(db, product['id'])
    return product

def _encoded_variants(variants):
    if not isinstance(variants, list):
        raise ValueError('variants must be a list')
    if not all(isinstance(variant, Mapping) for variant in variants):
        raise ValueError('each variant must be an object')
    encoded = [_encode(variant, VARIANT_ALLOWED) for variant in variants]
    if any(not values.get('name') for values in encoded):
        raise ValueError('variant name is required')
    return encoded


def _replace_variants(db, product_id, encoded_variants):
    """Replace variants that have already been validated and encoded."""
    db.execute('DELETE FROM variants WHERE product_id=?', (product_id,))
    for values in encoded_variants:
        columns = ['product_id', *values]
        db.execute(f"INSERT INTO variants ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})", [product_id, *values.values()])

def create(db, data):
    data = dict(data)
    variants = data.pop('variants', [])
    fields = _encode(data, ALLOWED)
    encoded_variants = _encoded_variants(variants)
    if not fields.get('sku') or not fields.get('name'):
        raise ValueError('sku and name are required')
    columns = ', '.join(fields)
    cursor = db.execute(f"INSERT INTO products ({columns}) VALUES ({', '.join('?' for _ in fields)})", list(fields.values()))
    _replace_variants(db, cursor.lastrowid, encoded_variants)
    db.commit()
    return get(db, cursor.lastrowid)

def get(db, product_id):
    return _product(db.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone(), db)

def list_products(db, search='', brand='', category='', status='', page=1, per_page=50):
    where, values = [], []
    if search:
        where.append('(name LIKE ? OR sku LIKE ?)'); values += [f'%{search}%', f'%{search}%']
    for field, value in [('brand', brand), ('category', category), ('status', status)]:
        if value:
            where.append(f'{field}=?'); values.append(value)
    clause = (' WHERE ' + ' AND '.join(where)) if where else ''
    total = db.execute('SELECT count(*) FROM products' + clause, values).fetchone()[0]
    rows = db.execute('SELECT * FROM products' + clause + ' ORDER BY id DESC LIMIT ? OFFSET ?', values + [per_page, (page - 1) * per_page]).fetchall()
    return {'items': [_product(row, db) for row in rows], 'total': total, 'page': page, 'per_page': per_page}

def update(db, product_id, data):
    data = dict(data)
    variants = data.pop('variants', None)
    fields = _encode(data, ALLOWED)
    encoded_variants = _encoded_variants(variants) if variants is not None else None
    if fields:
        db.execute('UPDATE products SET ' + ', '.join(f'{key}=?' for key in fields) + ", updated_at=CURRENT_TIMESTAMP WHERE id=?", [*fields.values(), product_id])
    if encoded_variants is not None and get(db, product_id) is not None:
        _replace_variants(db, product_id, encoded_variants)
    db.commit()
    return get(db, product_id)

def delete(db, product_id):
    deleted = db.execute('DELETE FROM products WHERE id=?', (product_id,)).rowcount > 0
    db.commit()
    return deleted
