from pwn import xor
flag = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
print(*[xor(flag,i) for i in range(256) if b"crypto{" in xor(flag,i)])