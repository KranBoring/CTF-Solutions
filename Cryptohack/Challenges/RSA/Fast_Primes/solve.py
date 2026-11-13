from sage.all import *
from Crypto.Util.number import sieve_base
from Crypto.PublicKey import RSA
from math import prod
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from Crypto.Cipher import PKCS1_OAEP
from time import time

def worker(task):
    chunk_start, chunk_end, e, best_M, N, inv_M, X_bound = task
    P = PolynomialRing(Zmod(N), names="x")
    x = P.gen()
    for a in range(chunk_start, chunk_end):
        rem = int(pow(e, a, best_M))
        f = x + (rem * inv_M) % N

        roots = f.small_roots(X=X_bound, beta=0.48, epsilon=0.03)
        if roots:
            x0 = int(roots[0])
            p_cand = int(best_M * x0 + rem)
            if N % p_cand == 0:
                return p_cand
    return None

def main():
    primes = sieve_base[:40]
    e = 0x10001
    orders = {p: int(Zmod(p)(e).multiplicative_order()) for p in primes}
    lcm_orders = lcm(list(orders.values()))
    best_M = None
    best_K = None
    for K in sorted(divisors(lcm_orders)):
        list_p = [p for p, o in orders.items() if K % o == 0]
        m_cand = prod(list_p)
        if m_cand.bit_length() > 140:
            best_M = m_cand
            best_K = K
            ord_best_M = lcm([o for o in orders.values() if best_K % o == 0])
            break
    
    data = RSA.importKey(open("key.pem").read())
    N = int(data.n)
    
    Z_best_M = Zmod(best_M)
    c = int(Z_best_M(N).log(Z_best_M(e)))

    X_bound = (2**256) // best_M + 1
    inv_M = int(pow(best_M, -1, N))

    tasks = []
    for c_start in range(c//2, (c//2 + ord_best_M)//2 + 1, 500):
        c_end = min(c_start + 500, (c//2 + ord_best_M)//2 + 1)
        tasks.append((c_start, c_end, e, best_M, N, inv_M, X_bound))
        
    print(f"log2(M') = {best_M.bit_length()}, chu kỳ = {ord_best_M}")

    p_found = None
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_task = {executor.submit(worker, task): task for task in tasks}
        for future in as_completed(future_to_task):
            res = future.result()
            if res is not None:
                p_found = res
                print(f"p = {p_found}")
                if executor._processes:
                    for process in list(executor._processes.values()):
                        try:
                            process.terminate()
                        except Exception:
                            pass
                executor.shutdown(wait=False, cancel_futures=True)
                break
    p = p_found
    q = N // p
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)

    key = RSA.construct((N, e, d))
    cipher = PKCS1_OAEP.new(key)
    ciphertext = bytes.fromhex(open("ciphertext.txt").read().strip())
    flag = cipher.decrypt(ciphertext)
    print(f"Flag :{flag.decode()}")

if __name__ == '__main__':
    start = time()
    main()
    print(f"Thời gian chạy: {(time() - start):.2f}")