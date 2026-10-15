import requests
from pwn import xor
url = "https://aes.cryptohack.org/flipping_cookie/"

s = requests.session()

def bytes2hex(data):
    return ''.join([f"{i:02x}" for i in data])

cookie = bytes.fromhex(s.get(f"{url}get_cookie/").json()["cookie"])
iv ,cookie = cookie[:16],cookie[16:]

blockplain1 = xor(b"admin=False;expi",iv)
new_iv = xor(blockplain1, b"admin=True;\x00expi")

cookie,new_iv = bytes2hex(cookie),bytes2hex(new_iv)

flag = s.get(f"{url}check_admin/{cookie}/{new_iv}/").json()["flag"]
print(flag)