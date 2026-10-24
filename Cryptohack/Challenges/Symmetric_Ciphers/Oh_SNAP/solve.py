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
import time

url = "https://aes.cryptohack.org/oh_snap/send_cmd/"
s = requests.session()

def get(ciphertext, nonce):
    ciphertext = ciphertext.hex()
    nonce = nonce.hex() 
    res = s.get(f"{url}{ciphertext}/{nonce}/")
    return res.json()

flag = b'crypto{'
ciphertext = b'\x00'
start = time.time()
while flag.endswith(b"}") != True:
    votes = [0 for _ in range(256)]
    for last_iv in range(256):
        iv = bytes([len(flag) + 3]) + b'\xff' + bytes([last_iv])
        first_bytes = bytes.fromhex(get(ciphertext, iv)["error"].split(' ')[-1])[0]
        cipher = RC4()
        votes[cipher.next_bytes(iv + flag, first_bytes)] += 1
    flag += bytes([votes.index(max(votes))])
    print(flag)
print(f"Thoi gian chay:{time.time() - start}")