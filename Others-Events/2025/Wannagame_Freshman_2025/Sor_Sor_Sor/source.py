import random

with open('flag.txt', 'rb') as f:
    flag = f.read().strip()

assert len(flag) % 3 == 0

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

blocks = [flag[i:i+3] for i in range(0, len(flag), 3)]
ori_blocks = [flag[i:i+3] for i in range(0, len(flag), 3)]

random.shuffle(blocks)

assert all(ori_blocks[i] != blocks[i] for i in range(len(blocks)))

print(xor(b''.join(blocks), flag).hex())
# 2f01090a6f042b4447101f0047460d6e0e5d001100422d156443022c4a3e074a392b033e531d1b47401b44423c411e08

