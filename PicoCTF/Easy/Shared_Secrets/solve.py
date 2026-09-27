from pwn import xor

enc = "b7b5b7b2b3bbafadb2be89a5e5b5a4e5a289b3e5efe3e2b4b3b4ab"
enc = bytes.fromhex(enc)
for i in range(256):
    flag = xor(enc, i)
    if b"academy{" in flag:
        print(flag)
        break