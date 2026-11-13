#!/usr/bin/env python3
import requests
from CTF_Crypto_Attack.Symmetric import craft_lazy_cbc_ciphertext, recover_lazy_cbc_key
def main() -> None:
    url = "https://aes.cryptohack.org/lazy_cbc/"
    s = requests.session()

    c_init = bytes.fromhex(s.get(f"{url}encrypt/{'aa'*48}/").json()["ciphertext"])

    payload = craft_lazy_cbc_ciphertext(c_init)

    res = s.get(f"{url}receive/{payload.hex()}/").json()
    leaked_pt = bytes.fromhex(res["error"].split(" ")[-1])

    key = recover_lazy_cbc_key(leaked_pt)

    flag_res = s.get(f"{url}get_flag/{key.hex()}/").json()
    
    print(bytes.fromhex(flag_res["plaintext"]).decode())
if __name__ == "__main__":
    main()