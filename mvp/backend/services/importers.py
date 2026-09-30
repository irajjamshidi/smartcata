import csv, io
from mvp.backend import crud
def import_csv(db, content: bytes):
    reader=csv.DictReader(io.StringIO(content.decode('utf-8-sig'))); summary={'rows':0,'imported':0,'updated':0,'rejected':0,'errors':[]}
    for row in reader:
        summary['rows']+=1
        if not row.get('sku') or not row.get('name'): summary['rejected']+=1; summary['errors'].append(f"row {summary['rows']}: sku and name required"); continue
        existing=db.execute('SELECT id FROM products WHERE sku=?',(row['sku'],)).fetchone()
        try:
            for n in ('cost','price'): row[n]=float(row.get(n) or 0)
            if existing: crud.update(db, existing['id'],row); summary['updated']+=1
            else: crud.create(db,row); summary['imported']+=1
        except Exception as error: summary['rejected']+=1; summary['errors'].append(f"row {summary['rows']}: {error}")
    return summary
