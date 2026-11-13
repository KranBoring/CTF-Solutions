#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import rail_fence_cipher
def main() -> None:
    ct = "Ta _7N6D86hlg:W3D_H3C31N__C16ef sHR053F38N43DE1 i33___NF"
    for rail in range(len(ct)):
        flag = rail_fence_cipher(ct, rail, 'd')
        if 'The flag' in flag:
            print(flag)
            break

if __name__ == "__main__":
    main()