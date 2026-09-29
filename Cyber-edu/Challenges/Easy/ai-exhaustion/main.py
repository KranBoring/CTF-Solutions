import os
import time


RSA_A = 7   
RSA_B = 13  

def get_aes_key() -> bytes:
    """Derive AES_KEY from flag.txt modification timestamp"""
    ts = int(os.path.getmtime("flag.txt"))
    return str(ts).encode()  

def xor_layer(data: bytes, key: bytes) -> bytes:
    return bytes([c ^ key[i % len(key)] for i, c in enumerate(data)])


def modinv(a: int, m: int = 256) -> int:
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        raise ValueError("a is not invertible")
    if t < 0:
        t += m
    return t

def affine_encrypt(data: bytes, a: int = RSA_A, b: int = RSA_B) -> bytes:
    return bytes([(a * c + b) % 256 for c in data])

B91_ALPHABET = [chr(i) for i in range(33, 124)] 

def base91_encode(data: bytes) -> str:
    out = []
    for b in data:
        hi = b // len(B91_ALPHABET)
        lo = b % len(B91_ALPHABET)
        out.append(B91_ALPHABET[hi] + B91_ALPHABET[lo])
    return ''.join(out)


def encrypt(plaintext: bytes, key: bytes) -> str:
    xored = xor_layer(plaintext, key)
    aff = affine_encrypt(xored)
    return base91_encode(aff)


if __name__ == "__main__":
    if not os.path.exists("flag.txt"):
        print("[-] flag.txt missing")
        exit(1)

    AES_KEY = get_aes_key()

    with open("flag.txt", "rb") as f:
        flag = f.read().strip()

    enc = encrypt(flag, AES_KEY)

    with open("cipher.txt", "w") as f:
        f.write(enc)

    print("[+] Ciphertext saved to cipher.txt")