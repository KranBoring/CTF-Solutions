import math

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))

def to_bytes(n):
    s = hex(n)
    s_n = s[2:]
    if 'L' in s_n:
        s_n = s_n.replace('L', '')
    if len(s_n) % 2 != 0:
        s_n = '0' + s_n
    decoded = bytes.fromhex(s_n)

    pad = (len(decoded) % BLOCK_SIZE)
    if pad != 0:
        decoded = b"\0" * (BLOCK_SIZE - pad) + decoded
    return decoded

def remove_line(s):
    # returns the header line, and the rest of the file
    return s[:s.index(b'\n') + 1], s[s.index(b'\n') + 1:]


def parse_header_ppm(f):
    data = f.read()

    header = b""

    for i in range(3):
        header_i, data = remove_line(data)
        header += header_i

    return header, data

def decrypt(ct):
    blocks = [ct[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE] for i in range(len(ct) // BLOCK_SIZE)]
    for i in range(len(blocks) - 1, 0, -1):
        prev_blk = int(blocks[i - 1].hex(), 16)
        curr_blk = int(blocks[i].hex(), 16)

        n_curr_blk = (prev_blk - curr_blk) % UMAX
        blocks[i] = to_bytes(n_curr_blk)

    ct_abc = b"".join(blocks[1:])
    return ct_abc

if __name__ == "__main__":
    with open('body.enc.ppm', 'rb') as f:
        header, data = parse_header_ppm(f)
    data_decrypt = decrypt(data)
    with open('flag.ppm','wb') as f:
        f.write(header)
        f.write(data_decrypt)
