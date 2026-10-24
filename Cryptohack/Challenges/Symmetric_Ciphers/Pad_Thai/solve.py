from pwn import *
from json import dumps, loads
import time

host = "socket.cryptohack.org"
port = 13421
io = remote(host, port)

def reline():
    res = io.recvline().strip().decode()
    return res

def sendl(payload):
    io.sendline(payload.encode())

def json_unpad(payload):
    return dumps({'option':'unpad','ct': payload.hex()})

def padding_attack(payload):
    sendl(json_unpad(payload))
    check = loads(reline())['result']
    return check

def xorn(m, number):
    return bytes([]) if m == b'' else bytes([a ^ number for a in m])

start = time.time()

reline()
sendl(dumps({"option":"encrypt"}))
data = bytes.fromhex(loads(reline())["ct"])

iv,ciphertext = data[:16], data[16:]
block_ciphertext = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

message = b''

for index in range(len(block_ciphertext) - 1, -1, -1):
    know_bytes = b''
    for count in range(16):
        payloads = [b'\x00' * (16 - count - 1) + bytes([i]) + xorn(know_bytes[::-1], count + 1) + block_ciphertext[index] for i in range(256)]
        bytes_index = 0
        while True:
            res = padding_attack(payloads[bytes_index])
            if res == True:
                message += bytes([(count + 1) ^ bytes_index])
                know_bytes += bytes([(count + 1) ^ bytes_index])
                break
            bytes_index += 1

message = message[::-1]
message = (xor(message[:16], iv) + xor(message[16:], block_ciphertext[0])).decode()

last_payload = dumps({'option':'check','message':message})
sendl(last_payload)
flag = reline()

print(flag)

print("Thoi gian chay:",time.time() - start)
