from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

m = "".join(choice(ascii_letters + digits) for _ in range(16))
q = getPrime(128)
p = getPrime(128)
n = q * p
e = 65537
d = inverse(e, (q - 1) * (e - 1))

c = pow(bytes_to_long(m.encode()), d, n)

print(f"{c = }")
print(f"{d = }")

print("vainglory?")
vainglory = input("> ").strip()

if vainglory == pride:
    print("Conquered!")
    with open("/challenge/flag.txt") as f:
        print(f.read())
else:
    print("Hubris!")
