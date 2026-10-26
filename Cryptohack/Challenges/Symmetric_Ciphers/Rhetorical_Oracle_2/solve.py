from pwn import *
from json import loads, dumps
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from os import urandom
from time import time

host = "socket.cryptohack.org"
port = 13437
io = remote(host, port)

def reline():
    return io.recvline().strip().decode()

def xorn(m, number):
    return bytes([]) if m == b'' else bytes([a ^ number for a in m])

def sendl(payload):
    io.sendline(payload.encode())

def json_unpad(payload):
    return dumps({'ciphertext': payload.hex()})

def padding_attack(payload, leng):
    io.send(payload.encode())
    res = []
    for i in range(leng):
        check = loads(reline())['good_pad']
        res.append(check)
    return res

CHUNK_BATCH = 12
def find_state(ciphertext):
    know_bytes = b''
    for count in range(16):
        payloads = [b'\x00' * (16 - count - 1) + bytes([i]) + xorn(know_bytes[::-1], count + 1) + ciphertext for i in range(256)]
        for i in range(0, 256, CHUNK_BATCH):
            batch = ''.join([json_unpad(payload) + '\n' for payload in payloads[i:i + CHUNK_BATCH]])
            leng = len(payloads[i:i + CHUNK_BATCH])
            res = padding_attack(batch, leng)
            if True in res:
                res = i + res.index(True)
                break
        know_bytes += bytes([(count + 1) ^ res])
    return know_bytes[::-1]
start = time()

#payload = dumps({"user_id": "0656d38b8cb0b41b82ecc9859cb7c03e53c7c6610bdce9ea14d30d1a33c80204"}).encode()
payload = '","user_id":"0656d38b8cb0b41b82ecc9859cb7c03e53c7c6610bdce9ea14d30d1a33c80204"}'.encode()
padded = pad(payload, AES.block_size)
P = [padded[i:i + 16] for i in range(0, len(padded), 16)]
blocks_payload = []

token = bytes.fromhex(loads(reline())['token'])
C_1_2 = token[:32]
C = urandom(16)
blocks_payload.append(C)
for index in range(len(P) - 1, -1, -1):
    I = find_state(C)
    C = xor(P[index], I)
    blocks_payload.append(C)
last_payload = C_1_2 + b''.join(blocks_payload[::-1])
print(last_payload)
sendl(json_unpad(last_payload))
flag = reline()
print(flag)
print(f'Thoi gian chay: {time() - start}')