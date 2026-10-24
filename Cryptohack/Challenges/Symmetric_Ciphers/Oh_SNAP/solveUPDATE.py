class RC4:
    def __init__(self):
        self.S = list(range(256))

    def swap(self, i, j):
        self.S[i], self.S[j] = self.S[j], self.S[i]
    
    def next_bytes(self, ivkey, keystream_bytes):
        j = 0
        leng = len(ivkey)
        for i in range(leng):
            j = (j + self.S[i] + ivkey[i]) % 256
            self.swap(i, j)
        return (self.S.index(keystream_bytes) - j - self.S[leng]) % 256
            
import requests
from pwn import xor
from concurrent.futures import ThreadPoolExecutor
import time

url = "https://aes.cryptohack.org/oh_snap/send_cmd/"

def payload(tuple):
    last_iv, leng = tuple[0], tuple[1]
    payload = bytes([leng + 3, 0xff, last_iv])
    res = bytes.fromhex(requests.get(f"{url}00/{payload.hex()}/").json()["error"].split(' ')[-1])[0]
    return (last_iv, res)

flag = b'crypto{'
start = time.time()
while flag.endswith(b"}") != True:
    votes = [0 for _ in range(256)]
    payloads = [(last_iv, len(flag)) for last_iv in range(256)]
    with ThreadPoolExecutor(max_workers = 256) as f:
        server_res = f.map(payload, payloads)
    for last_iv, first_bytes in server_res:
        iv = bytes([len(flag) + 3, 0xff, last_iv])
        cipher = RC4()
        votes[cipher.next_bytes(iv + flag, first_bytes)] += 1
    flag += bytes([votes.index(max(votes[:256]))])
    print(flag)
print(f"Thoi gian chay:{time.time() - start}")