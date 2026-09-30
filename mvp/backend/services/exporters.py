import csv, io
def export_csv(items):
    fields=['id','sku','name','brand','category','status','cost','price','currency']; out=io.StringIO(); writer=csv.DictWriter(out,fieldnames=fields); writer.writeheader(); writer.writerows({k:i.get(k,'') for k in fields} for i in items); return out.getvalue()
