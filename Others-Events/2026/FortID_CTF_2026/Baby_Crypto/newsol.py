from Crypto.Util.number import *
from Crypto.Cipher import AES
from pwn import *
import json

host = "baby-crypto-1cbce27c9c7c.inst16.ctf.fortid.com"
port = 1337

def reuntil(text):
    res = io.recvuntil(text.encode())
    print(res.decode())
def payload(payload):
    io.sendline(payload)
    print(payload)

format = b"FortID{S"
cipher_len = 70
payload_plain = format + b"\x00"*(cipher_len-8)
io = remote(host, port, ssl = True)
reuntil(">")
payload(b"1")
reuntil("Enter secret:")
payload(payload_plain)
reuntil(">")
payload(b"2")
json_data = json.loads(io.recvline().strip().decode())
print(json_data)
print(xor(bytes.fromhex(json_data["Secret #0"]),bytes.fromhex(json_data["Secret #1"])))
