import json
ALLOWED={'sku','name','slug','brand','category','model','description','status','image','attributes','cost','price','currency'}
def create(db, data):
    fields={k:(json.dumps(v, ensure_ascii=False) if k=='attributes' and not isinstance(v,str) else v) for k,v in data.items() if k in ALLOWED}
    cols=', '.join(fields); cur=db.execute(f"INSERT INTO products ({cols}) VALUES ({', '.join('?' for _ in fields)})", list(fields.values())); db.commit(); return get(db,cur.lastrowid)
def get(db, product_id):
    row=db.execute('SELECT * FROM products WHERE id=?',(product_id,)).fetchone(); return dict(row) if row else None
def list_products(db, search='', brand='', category='', status='', page=1, per_page=50):
    where=[]; vals=[]
    if search: where.append('(name LIKE ? OR sku LIKE ?)'); vals += [f'%{search}%',f'%{search}%']
    for field,value in [('brand',brand),('category',category),('status',status)]:
        if value: where.append(f'{field}=?'); vals.append(value)
    clause=(' WHERE '+' AND '.join(where)) if where else ''
    total=db.execute('SELECT count(*) FROM products'+clause,vals).fetchone()[0]
    rows=db.execute('SELECT * FROM products'+clause+' ORDER BY id DESC LIMIT ? OFFSET ?', vals+[per_page,(page-1)*per_page]).fetchall()
    return {'items':[dict(r) for r in rows], 'total':total, 'page':page, 'per_page':per_page}
def update(db, product_id, data):
    fields={k:(json.dumps(v,ensure_ascii=False) if k=='attributes' and not isinstance(v,str) else v) for k,v in data.items() if k in ALLOWED}
    if not fields: return get(db, product_id)
    db.execute('UPDATE products SET '+', '.join(f'{k}=?' for k in fields)+", updated_at=CURRENT_TIMESTAMP WHERE id=?",list(fields.values())+[product_id]); db.commit(); return get(db,product_id)
def delete(db, product_id):
    return db.execute('DELETE FROM products WHERE id=?',(product_id,)).rowcount > 0
