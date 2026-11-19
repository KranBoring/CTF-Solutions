import hashlib
import sys
from sage.all import *
from time import time

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("53c1beea6e427b3de1acf4834baed794f4bbd0dfe1d85f6a248ba4c12b")

# This will overflow the stack, it will need to be significantly optimized in order to get the answer :)
'''
@functools.cache
def m_func(i):
    if i == 0: return 1
    if i == 1: return 2
    if i == 2: return 3
    if i == 3: return 4

    return 55692*m_func(i-4) - 9549*m_func(i-3) + 301*m_func(i-2) + 21*m_func(i-1)
'''
def m_func(i):
    S_base = vector(QQ, [4, 3, 2 ,1])
    M = Matrix(QQ, 4, 4, [21, 301, -9549, 55692, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0])

    start = time()
    S_i = M**(i - 3) * S_base
    end1 = time()
    print(f"Thời gian chạy: {end1- start}")

    D, P = M.eigenmatrix_right()
    S_i = P * D**(i - 3) * P**-1 * S_base
    print(f"Thời gian chạy: {time()- end1}")
    return int(S_i[0])
# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)

if __name__ == "__main__":
    sol = m_func(ITERS)
    decrypt_flag(sol)
