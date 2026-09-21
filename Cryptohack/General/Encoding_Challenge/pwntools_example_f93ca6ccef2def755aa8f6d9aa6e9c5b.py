from pwn import * # pip install pwntools
import json
import base64
import codecs
from Crypto.Util.number import *

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

for i in range(100):
    received = json_recv()

    print("Received type: ")
    print(received["type"])
    print("Received encoded value: ")
    print(received["encoded"])
    decode = ""
    if received["type"] == "base64":
        decode = base64.b64decode(received["encoded"].encode()).decode()
    elif received["type"] == "hex":
        decode = bytes.fromhex(received["encoded"]).decode()
    elif received["type"] == "rot13":
        decode = codecs.decode(received["encoded"], 'rot_13')
    elif received["type"] == "bigint":
        decode = long_to_bytes(int(received["encoded"],16)).decode()
    elif received["type"] == "utf-8":
        for i in received["encoded"]:
            decode += chr(i)
    
    to_send = {
        "decoded": decode
    }
    json_send(to_send)

json_recv()
