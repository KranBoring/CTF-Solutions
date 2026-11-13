import requests
from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from ecdsa import SigningKey, SECP256k1
from json import dumps

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

class chall:
    def __init__(self):
        self.url = "http://w01.ctf.chronos-security.ro:36776"
        self.s = requests.session()
    def schema(self):
        res = self.s.get(f"{self.url}/schema")
        return res
    def pubkey(self):
        res = self.s.get(f"{self.url}/pubkey")
        return res
    def receipts(self):
        res = self.s.get(f"{self.url}/receipts")
        return res
    def authorize(self, json):
        body = dumps(payload, separators=(',', ':'))
        res = requests.post(f"{self.url}/authorize", data=body, headers={'Content-Type': 'application/json'})
        return res
def return_value(sig):
    m = bytes.fromhex(sig['message_hex'])
    z = bytes_to_long(sha256(m).digest())
    r = int(sig['r'], 16)
    s = int(sig['s'], 16)
    return z, r, s
c = chall()
sig1, sig2 = c.receipts().json()['receipts']
z1, r1, s1 = return_value(sig1)
z2, r2, s2 = return_value(sig2)
k = (z1 - z2) * pow(s1 - s2, -1, n) % n
d = (pow(r1, -1, n) * (s1 * k - z1)) % n
payload_message = bytes.fromhex(c.schema().json()['master_message_hex'])
sk = SigningKey.from_secret_exponent(d, curve=SECP256k1)
sig = sk.sign(payload_message, hashfunc=sha256)

payload_sig = sk.sign_deterministic(payload_message, hashfunc=sha256)
r = bytes_to_long(payload_sig[:32])
s = bytes_to_long(payload_sig[32:])
if s > n // 2:
    s = n - s

payload = {"message_hex":payload_message.hex(),"r":f"{r:064x}","s":f"{s:064x}"}
print(c.authorize(payload).text)

    