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

format = b"FortID{"
for char1 in range(2,7):
    io = remote(host, port, ssl = True)
    for char2 in range(16):
        reuntil(">")
        payload(b"1")
        reuntil("Enter secret:")
        payload(format + long_to_bytes(char1*16+char2))
    reuntil(">")
    payload(b"2")
    json_data = json.loads(io.recvline().strip().decode())
    print(json_data)
    ciphertext = bytes.fromhex(json_data["Secret #0"])
    for index in range(1,len(json_data)):
        xored = xor(ciphertext[:8],bytes.fromhex(json_data[f"Secret #{index}"])[:8])
        print(f"Ma: {(char1 * 16 + index-1)}, ASCII: {long_to_bytes(char1 * 16 + index-1)}, xored: {xored}")
        print(format + long_to_bytes((char1 * 16 + index-1)))
    io.close()
io = remote(host, port, ssl = True)
for char in range(113, 127):
    reuntil(">")
    payload(b"1")
    reuntil("Enter secret:")
    payload(format + long_to_bytes(char))
reuntil(">")
payload(b"2")
json_data = json.loads(io.recvline().strip().decode())
print(json_data)
ciphertext = bytes.fromhex(json_data["Secret #0"])
for index in range(1,len(json_data)):
    xored = xor(ciphertext[:8],bytes.fromhex(json_data[f"Secret #{index}"])[:8])
    print(f"Ma: {(index + int("70",16))-1}, ASCII: {long_to_bytes((index + int("70",16)))-1}, xored: {xored}")
    print(format + long_to_bytes(index + int("70",16)-1))
io.close()



