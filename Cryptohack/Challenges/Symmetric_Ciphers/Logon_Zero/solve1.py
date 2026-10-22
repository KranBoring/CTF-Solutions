from pwn import *
import json
from Crypto.Util.number import bytes_to_long

host = "socket.cryptohack.org"
port = 13399

io = remote(host, port)

def sendl(payload):
    io.sendline(payload)
    print(payload.decode())

def reline():
    res = io.recvline().strip().decode()
    print(res)
    return res

def auto_json(dict):
    return json.dumps(dict).encode()

reline()
while True:
    payload = auto_json({"option": 'reset_password',"token":"00" * 28})
    sendl(payload)
    reline()

    for i in range(0x20,0x7e):
        char_bytes = bytes([i]) * 12
        new_password = char_bytes[:-4]
        length_password = bytes_to_long(char_bytes[-4:])
        password = new_password[:length_password].decode()
        new_payload = auto_json({'option':'authenticate','password': password})
        sendl(new_payload)
        res = json.loads(reline())['msg']
        if "crypto{" in res:
            break
    if "crypto{" in res:
        print(res)
        io.close()
        break
    payload = auto_json({'option': 'reset_connection'})
    sendl(payload)
    reline()