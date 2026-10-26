from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from json import JSONDecodeError, dumps, loads
from secrets import token_bytes, token_hex

from utils import listener

ADMINS = ["0656d38b8cb0b41b82ecc9859cb7c03e53c7c6610bdce9ea14d30d1a33c80204",
          "3cc87cad6be102200df733cfa33e02889ce798a88470f3aa2e59bebcaee054b3"]
FLAG = "crypto{?????????????????????????}"
TOKEN_SIZE = 32


def decrypt(key, iv, ciphertext):
    aes_cbc = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = aes_cbc.decrypt(ciphertext)
    try:
        plaintext = unpad(plaintext, AES.block_size)
    except ValueError:
        good_pad = False
    else:
        good_pad = True
    return plaintext, good_pad


class Challenge(object):
    def __init__(self):
        # A forged token runs to several blocks of hex, which overflows the
        # default 1024 byte limit and would otherwise drop the connection.
        self.max_payload_size = 4096
        user_id = token_hex(TOKEN_SIZE)
        # Even improbable events can still happen, so check that admin session tokens aren't granted to users.
        while user_id in ADMINS:    
            user_id = token_hex(TOKEN_SIZE)
        plaintext = dumps({"user_id": user_id}).encode()
        padded = pad(plaintext, AES.block_size)
        self.key = token_bytes(AES.key_size[2])
        self.iv = token_bytes(AES.block_size)
        aes_cbc = AES.new(self.key, AES.MODE_CBC, iv=self.iv)
        ciphertext = aes_cbc.encrypt(padded)
        dumped = dumps({"token": ciphertext.hex()})
        self.before_input = f"{dumped}\n"

    def challenge(self, your_input):
        ciphertext = your_input.get("ciphertext")
        ciphertext = bytes.fromhex(ciphertext)
        plaintext, good_pad = decrypt(self.key, self.iv, ciphertext)
        if good_pad:
            try:
                decoded = plaintext.decode("unicode_escape")
                token = loads(decoded, strict=False)
                if token["user_id"] in ADMINS:
                    return {"flag": FLAG}
            except (JSONDecodeError, UnicodeDecodeError, TypeError, KeyError):
                return {"good_pad": good_pad}
        return {"good_pad": good_pad}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13437)
