import csv

def csv_read(filename):
    with open(filename,newline='',encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        data = bytearray()
        for r in reader:
            value = r['NLRI prefix']
            if not value:
                continue
            data.extend(int(oc) for oc in value.split('.'))
    return data.decode('ascii')
print(csv_read("1010101.csv"))
print(csv_read("101010251.csv"))