from pwn import *
from json import dumps, loads
import time

host = "socket.cryptohack.org"
port = 13422
io = remote(host, port)

def reline():
    res = io.recvline().strip().decode()
    return res

def sendl(payload):
    io.sendline(payload.encode())

def json_unpad(payload):
    return dumps({'option':'unpad','ct': payload.hex()}, separators=(',', ':'))

def padding_attack(payload, leng):
    io.send(payload.encode())
    res = []
    for i in range(leng):
        check = loads(reline())['result']
        res.append(check)
    return res

def xorn(m, number):
    return bytes([]) if m == b'' else bytes([a ^ number for a in m])

start = time.time()

reline()
sendl(dumps({"option":"encrypt"}))
data = bytes.fromhex(loads(reline())["ct"])

iv,ciphertext = data[:16], data[16:]
block_ciphertext = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

full_block = [iv] + block_ciphertext
HEX = b"1234567890abcdef"

message = b''
CHUNK_BATCH = 1

for index in range(len(block_ciphertext) - 1, -1, -1):
    know_bytes = b''
    prev_block = full_block[index]
    for count in range(16):
        pos = 15 - count
        list_bytes = [c ^ prev_block[pos] ^ (count + 1) for c in HEX]
        payloads = [b'\x00' * pos + bytes([i]) + xorn(know_bytes[::-1], count + 1) + block_ciphertext[index] for i in list_bytes]
        for i in range(0, 16, CHUNK_BATCH):
            res = []
            for _ in range(2):
                batch = ''.join([(json_unpad(payload) + '\n') * 10 for payload in payloads[i:i + CHUNK_BATCH]])
                leng = len(payloads[i:i + CHUNK_BATCH]) * 10
                res += padding_attack(batch, leng)
                if False in res:
                    break
            if False in res:
                continue
            else:
                res = list_bytes[i]
                break
        message += bytes([(count + 1) ^ res])
        know_bytes += bytes([(count + 1) ^ res])

message = message[::-1]
message = (xor(message[:16], iv) + xor(message[16:], block_ciphertext[0])).decode()

last_payload = dumps({'option':'check','message':message})
sendl(last_payload)
flag = reline()

print(flag)

print("Thoi gian chay:",time.time() - start)
