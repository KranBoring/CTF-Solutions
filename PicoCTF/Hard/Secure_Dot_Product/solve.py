#!/usr/bin/env python3
# %%
from time import sleep
from CTF_Crypto_Attack.Util import BaseSocketOracle, parsers
from CTF_Crypto_Attack.Hash import new
from ast import literal_eval
from pwn import remote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Oracle(BaseSocketOracle):
    def get_iv_ct(self):
        self.io.recvline()
        return parsers((self.io.recvline() + self.io.recvline()).strip().decode(), parse_hex=True).values()
    def get_5_vector(self):
        self.io.recvline()
        self.io.recvline()
        self.io.recvline()
        vectors = []
        for _ in range(5):
            vectors.append(literal_eval(self.io.recvline().strip().decode()))
        return vectors
    def get_dot_product(self, list: str, hash: str):
        self.io.recvuntil(b":")
        self.io.sendline(list.encode())
        self.io.recvuntil(b":")
        self.io.sendline(hash.encode())
        self.io.recvuntil(b":")
        dot = self.io.recvline().strip().decode()
        print(dot)
        return literal_eval(dot)
def main() -> None:
    check = False
    while True:
        while True:
            try:
                io = remote("xebec.cylabacademy.net", 35347)
                break
            except Exception:
                sleep(2)
        oracle = Oracle(io)
        iv, ciphertext = oracle.get_iv_ct()
        vectors = oracle.get_5_vector()
        vectors = sorted(vectors, key=lambda vector: len(vector[0]))
        if len(vectors[0][0]) == 1:
            for index in range(1, len(vectors)):
                if (len(vectors[index][0]) - len(vectors[index - 1][0])) <= 8:
                    if len(vectors[index][0]) + 8 >= 32:
                        check = True
                        break
                    else:
                        continue
                else:
                    break
        if check:
            break
        io.close()

    diff_len = [len(vectors[index][0]) - len(vectors[index - 1][0]) for index in range(1, len(vectors))] + [32 - len(vectors[-1][0])]
    print(diff_len)
    key = bytearray()
    key += bytes([oracle.get_dot_product(str(vectors[0][0]), vectors[0][1]) // abs(vectors[0][0][0])])

    def solve(vector_tuple, key, diff_len):

        vector = vector_tuple[0]
        vector_hash = vector_tuple[1]

        base_dot = oracle.get_dot_product(str(vector), vector_hash)

        hasher = new('sha512')
        new_vector, vector_hash = hasher.extension(
            secret_length=256,
            original_data=str(vector)[1:-1].encode('latin-1'),
            append_data=b', 1',
            signature=vector_hash
        )

        new_vector_send = str(new_vector)[2:-1]
        diff = oracle.get_dot_product(f"[{new_vector_send}]", vector_hash) - base_dot
        key += bytes([diff])
        if len(key) == 32:
            return key
        base_dot += diff
        for _ in range(len(key), len(key) + diff_len - 1):
            hasher = new('sha512')
            new_vector, vector_hash = hasher.extension(
                secret_length=256,
                original_data=new_vector,
                append_data=b', 1',
                signature=vector_hash
            )
            new_vector_send = str(new_vector)[2:-1]
            diff = oracle.get_dot_product(f"[{new_vector_send}]", vector_hash) - base_dot
            key += bytes([diff])
            if len(key) == 32:
                return key
            base_dot += diff
        return key
    for vector, diff in zip(vectors, diff_len):
        key = solve(vector, key, diff)
        if len(key) == 32:
            break
    print(key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(ciphertext)
    print(unpad(flag, 16))
if __name__ == "__main__":
    main()
# %%
