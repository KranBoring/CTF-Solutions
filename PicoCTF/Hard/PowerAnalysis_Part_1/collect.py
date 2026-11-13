from pwn import *
from ast import literal_eval
from os import urandom
import numpy as np

host = "chatelaine.cylabacademy.net"
port = 33933
context.log_level = "error"


def collect():
    plaintexts = []
    traces = []
    for idx in range(300):
        io = remote(host, port)
        plaintext = urandom(16)
        io.recvuntil(b":")
        io.sendline(plaintext.hex().encode())
        io.recvuntil(b":")
        res = io.recvline().strip().decode()
        io.close()
        trace = literal_eval(res)

        plaintexts.append(list(plaintext))
        traces.append(trace)
    np.save("plaintexts.npy", np.array(plaintexts, dtype=np.uint8))
    np.save("traces.npy", np.array(traces, dtype=np.float64))

if __name__ == "__main__":
    collect()

