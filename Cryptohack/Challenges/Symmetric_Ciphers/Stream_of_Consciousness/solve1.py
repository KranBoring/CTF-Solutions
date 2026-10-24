from pwn import xor

plain = "How proud and happy he'll be when he gets my note!".encode()
cipher = bytes.fromhex("9503f3141b9bdf7ed4ddaeb529f2d2a3ec3961b08b581a89fd151af20791fb99057de1298e01e8a44c4b8f13922fa668aa4b")
cipher_flag = bytes.fromhex("be1efd441f86cb608384faec3fe18eafc33b2be5d60e62d4a46a1ea310d2ff81")
keystream = xor(cipher, plain)
flag = xor(cipher_flag, keystream)
print(flag)