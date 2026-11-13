#!/usr/bin/env python3
import requests
from CTF_Crypto_Attack.Symmetric.aes_modes import bit_flip_cbc
def main() -> None:
    url = "https://aes.cryptohack.org/flipping_cookie/"
    s = requests.session()
    cookie = bytes.fromhex(s.get(f"{url}get_cookie/").json()["cookie"])
    iv ,cookie = cookie[:16],cookie[16:]
    pt = b"admin=False;expiry="
    new_plaintext = b"admin=True;\x00expi"
    old_plaintext = b"admin=False;expi"
    offset = pt.find(old_plaintext)
    new_iv,new_cookie = bit_flip_cbc(
        ciphertext=cookie,
        offset=offset,
        orig_text=old_plaintext,
        new_text=new_plaintext,
        iv=iv
    )
    new_cookie,new_iv = (new_cookie).hex(), (new_iv).hex()

    flag = s.get(f"{url}check_admin/{new_cookie}/{new_iv}/").json()["flag"]
    print(flag)


if __name__ == "__main__":
    main()