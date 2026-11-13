import random
from Crypto.Util.number import isPrime, long_to_bytes
from CTF_Crypto_Attack import RSA

C = 0x42c2b662d2c1e70dd9cccd665edfe9a6069dd031a5b0ddf904a819b90581ffd61c89eb1b1a1878acf3b6b45c8d5177796a4323f079ddf4e7f668410306c1d04a6a995154a03f7257f8f89584ea1a6e3bb291d58893ae140dbf70f111c2f855d686aca122996eb4453fa39a701e23471d516b9b42b78c3d73a9ca300beece078e
serial = 6631 
e = 65537
N = 0x638c4593a4d52f4be3825d8c8193ccd9551aea1e1a047adb0db7907958e127c6ee53a926e982f602e0407e43eb14cb927f0e541543418256011fa132945f14e1a70cdf1ef277e9851219c8b93004fb29233e16bf51886108b0ee750151602cb2a6d56252adfd6c00159cbf4111a1fa4e14c4809008cf455fcccd78c9a24773af
timestamp = 1699994070

def get_prime():
    while True:
        cand = random.getrandbits(512) | (1 << 511) | 1
        if isPrime(cand):
            return cand

found = False
for i in range(0, 10000):
    for j in [-1, 1]:
        t = timestamp + i * j
        seed = (t << 16) | serial
        random.seed(seed)
        p = get_prime()
        if N % p == 0:
            q = N // p
            flag = RSA.decrypt(C, e=e, factors=[q, p], advanced_mode=True)
            print(flag)
            found = True
            break
    if found:
        break