from json import dumps, loads
from CTF_Crypto_Attack.DH_DLP import craft_smooth_dh_params, pohlig_hellman
from pwn import remote
from decrypt import decrypt_flag

io = remote("socket.cryptohack.org",13378)

def ut(text = ":"):
    io.recvuntil(text.encode())

def rejson():
    return loads(io.recvline().strip().decode())

def main():
    ut()
    p, g, A = map(int, rejson().values(), [16, 16, 16])
    ut()
    B = int(rejson()['B'], 16)
    ut()
    iv, ciphertext = rejson().values()
    ut()
    p_, g_, A_, cyclic_g = craft_smooth_dh_params(1600)
    json = dumps({"p":f"0x{p_:02x}","g":f"0x02","A":f"0x{A:02x}"}).encode()
    io.sendline(json)
    ut()
    new_B = int(rejson()['B'], 16)
    b = pohlig_hellman(g_, new_B, p_, cyclic_g)
    S = pow(A, b, p)
    flag = decrypt_flag(S, iv, ciphertext)
    print(flag)

if __name__ == "__main__":
    main()