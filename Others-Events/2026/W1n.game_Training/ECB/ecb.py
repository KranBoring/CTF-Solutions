# Install dependencies: pip install pycryptodome
# Hint: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)

import secrets

from Crypto.Cipher import AES

with open("flag.txt", "rb") as f:
    FLAG = f.read().strip()

assert len(FLAG) == 32

def main() -> None:
    key_int = secrets.randbelow(1_000_001) 
    key = key_int.to_bytes(16, "big")

    ct = AES.new(key, AES.MODE_ECB).encrypt(FLAG)
    with open("output.txt", "w") as f:
        f.write(ct.hex())


if __name__ == "__main__":
    main()


# ct: a58fd383d77105ed4cec2ff0eb3e483dea0d8bf2d963ce6e61a7c875a8b4edea
