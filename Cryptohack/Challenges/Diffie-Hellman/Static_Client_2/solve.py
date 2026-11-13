from json import dumps, loads
from Crypto.Util.number import isPrime
from pwn import remote
from decrypt import decrypt_flag
from sage.all import discrete_log, GF

io = remote("socket.cryptohack.org",13378)

def ut(text = ":"):
    io.recvuntil(text.encode())

def rejson():
    return loads(io.recvline().strip().decode())

def smooth_p(p):
    mul = 1
    i = 1
    while 1:
        mul *= i
        if (mul + 1).bit_length() >= p.bit_length() and isPrime(mul + 1):
            return mul + 1
        i += 1
def main():
    ut()
    p, g, A = map(int, rejson().values(), [16, 16, 16])
    ut()
    B = int(rejson()['B'], 16)
    ut()
    iv, ciphertext = rejson().values()
    ut()
    p_ = smooth_p(p)
    json = dumps({"p":f"0x{p_:02x}","g":f"0x02","A":f"0x{A:02x}"}).encode()
    io.sendline(json)
    ut()
    new_B = int(rejson()['B'], 16)
    b = discrete_log(GF(p_)(new_B), GF(p_)(g))
    S = pow(A, b, p)
    flag = decrypt_flag(S, iv, ciphertext)
    print(flag)

if __name__ == "__main__":
    main()


