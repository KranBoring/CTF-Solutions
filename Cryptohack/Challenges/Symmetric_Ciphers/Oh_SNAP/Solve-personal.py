from CTF_Crypto_Attack.Symmetric import fms_rc4
from CTF_Crypto_Attack.Util import BaseHttpOracle

class Oracle(BaseHttpOracle):
    def get_first_keystream_byte(self, iv):
        res = self.session.get(f"{self.base_url}00/{iv.hex()}/").json()
        return bytes.fromhex(res["error"].split(" ")[-1])[0]
def main():
    oracle = Oracle("https://aes.cryptohack.org/oh_snap/send_cmd/", 256)
    flag = fms_rc4(
        oracle=oracle,
        known_prefix=b"crypto{",
        max_workers=256
	)
    print(flag)

if __name__ == '__main__':
    main()
        