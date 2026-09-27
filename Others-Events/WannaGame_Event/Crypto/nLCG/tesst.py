from Crypto.Util.number import inverse, isPrime
import math
x1 = 94953608618212798825709752424748009864970688661922235543439920722999382561264
x2 = 66266231073687781242323989167201000615114581526380783004510961476024126407247
x3 = 2104811219174241508218775035711318490841432526449341354491786430727766387787
x4 = 43868577857177529013047921323762260736987468235480252629230360715726175868943
x5 = 6452282319344224581403088491468753749075925552250193778565441733982960058434
deltaX2 = x2-x1
deltaX3 = x3-x2
deltaX4 = x4-x3
deltaX5 = x5-x4

detA1 = (deltaX4 * deltaX2) - pow(deltaX3,2)
detA2 = (deltaX5 * deltaX3) - pow(deltaX4,2)
m = math.gcd(abs(detA1), abs(detA2))

# 1. Tẩy rửa m "bẩn" (Loại bỏ các hệ số ký sinh của GCD)
for i in range(2, 10000):
    while m % i == 0 and not isPrime(m):
        m = m // i
print(f"[*] Modulus m tinh khiết: {m}")

# 2. Ép không gian Modulo để chống crash số âm
a = (deltaX3 % m) * inverse(deltaX2 % m, m) % m
print(f"[*] Hệ số nhân a: {a}")

c = (x2 - a * x1) % m
print(f"[*] Bước nhảy c: {c}")

print("[+] Bắt đầu bypass server Part 1:")
for i in range(3):
    x5 = (a * x5 + c) % m
    print(x5)