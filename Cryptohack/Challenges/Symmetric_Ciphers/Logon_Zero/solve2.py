from pwn import *
import json

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
    payload = auto_json({'option':'authenticate','password': ""})
    sendl(payload)
    res = json.loads(reline())['msg']
    if "crypto{" in res:
        print(res)
        io.close()
        break
    payload = auto_json({'option': 'reset_connection'})
    sendl(payload)
    reline()