from Crypto.PublicKey import ECC

with open("sealed-orders.der","rb") as f:
    data = ECC.import_key(f.read())
