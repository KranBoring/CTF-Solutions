#!/usr/bin/env python3
# %%
from CTF_Crypto_Attack.Util import BaseSocketOracle, parsers
from CTF_Crypto_Attack.Symmetric import recover_poly1305_key, forge_poly1305_tag
from pwn import remote

io = remote("xebec.cylabacademy.net", 32195)
goal = b"But it's only secure if used correctly!"

class Oracle(BaseSocketOracle):
    def get_all(self):
        return parsers(self.io.recv().strip().decode(), parse_hex=True, multi_value=True, normalize_keys=True).values()

def main() -> None:
    oracle = Oracle(io)
    plaintext, plaintext_hex, ciphertext_hex = oracle.get_all()

    C1, T1, N1 = ciphertext_hex[0][:-28], ciphertext_hex[0][-28:-12], ciphertext_hex[0][-12:]
    C2, T2, N2 = ciphertext_hex[1][:-28], ciphertext_hex[1][-28:-12], ciphertext_hex[1][-12:]

    r, s = recover_poly1305_key(C1, T1, C2, T2)

    keystream = bytes(a ^ b for a, b in zip(C1, plaintext_hex[0]))
    C_goal = bytes(a ^ b for a, b in zip(goal, keystream))

    T_goal = forge_poly1305_tag(r, s, C_goal)
    
    payload = C_goal + T_goal + N1
    io.sendline(payload.hex().encode())
    print(io.recvall().strip().decode())
if __name__ == "__main__":
    main()

# %%
