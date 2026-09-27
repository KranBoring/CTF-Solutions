import os
import sys

from Crypto.Util.number import getPrime
from random import randint

# Public parameters
g = 2
p = getPrime(1048)

# Server's secret
a = randint(2, p-2)
A = pow(g, a, p)

# Client secret
b = randint(2, p-2)

B = pow(g, b, p)

# Shared key
shared = pow(A, b, p)

# Encrypt flag
flag = b"academy{...}"
enc = bytes([x ^ (shared % 256) for x in flag])

# Write challenge info
#
# You were handed message.txt alongside this script, and this writes that same
# name. Running it here would overwrite the file you have to solve with a fresh
# transcript over the redacted flag above -- a different p and b, and nothing to
# recover. So refuse rather than clobber.
if os.path.exists("message.txt"):
    sys.exit("message.txt already exists here -- that is the file you were given, "
             "and running this would overwrite it. Move it aside first, or run "
             "this somewhere else.")

with open("message.txt", "w") as f:
    f.write(f"g = {g}\n")
    f.write(f"p = {p}\n")
    f.write(f"A = {A}\n")
    f.write(f"b = {b}\n")
    f.write(f"enc = {enc.hex()}\n")
