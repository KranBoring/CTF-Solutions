from json import load
from base64 import b64decode
from hashlib import sha256
from Crypto.Util.number import bytes_to_long
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
with open('signing-export.json', 'r') as f:
    data = load(f)
def return_value(record):
    raw_msg = b64decode(record['message_b64'])
    z = bytes_to_long(sha256(raw_msg).digest())
    sig = bytes.fromhex(record['signature_rs_hex'])
    r = bytes_to_long(sig[:32])
    s = bytes_to_long(sig[32:])
    return z, s, r
records = data['records']
id6103 = records[2]
id6107 = records[6]
z1, s1, r = return_value(id6103)
z2, s2, _ = return_value(id6107)
k = (z1 - z2) * pow(s1 - s2, -1, n) % n
d = (pow(r, -1, n) * (s1 * k - z1)) % n
print(f"{d:064x}")
