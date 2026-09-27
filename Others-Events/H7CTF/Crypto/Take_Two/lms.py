#!/usr/bin/env python3
# a compact LMS-style hash-based signature: WOTS one-time leaves under a Merkle
# tree (RFC 8554 in spirit, self-consistent hashing). this is the signer the
# firmware server uses; it is shipped so the scheme is known. the vulnerability
# is operational (a leaf reused via a counter reset), not in this code.
import hashlib

N = 32          # sha256 output bytes
W = 16          # winternitz parameter (4-bit digits)
LEN1 = 64       # message digits (256 bits / 4)
LEN2 = 3        # checksum digits
LEN = LEN1 + LEN2
TREE_H = 4      # 16 one-time leaves

def H(b):
    return hashlib.sha256(b).digest()

def chain(x, steps): # Hash sha256 step lần trên 1 chuỗi
    for _ in range(steps):
        x = H(x)
    return x

def msg_digits(msg):
    d = H(msg)
    digs = []
    for byte in d:
        digs.append(byte >> 4)
        digs.append(byte & 0xF)
    c = sum(W - 1 - x for x in digs)          # winternitz checksum
    digs += [(c >> 8) & 0xF, (c >> 4) & 0xF, c & 0xF]
    return digs                                # length LEN

def wots_pk(sk):                               # sk: list[LEN] of N-byte secrets
    return H(b"".join(chain(s, W - 1) for s in sk))

def wots_sign(sk, msg):
    return [chain(sk[i], d) for i, d in enumerate(msg_digits(msg))]

def wots_pk_from_sig(msg, sig):                # recompute the leaf public key
    return H(b"".join(chain(sig[i], W - 1 - d) for i, d in enumerate(msg_digits(msg))))

def merkle(leaves):                            # returns (root, levels) ; leaves: list[2^TREE_H]
    levels = [leaves]
    cur = leaves
    while len(cur) > 1:
        cur = [H(b"\x01" + cur[i] + cur[i + 1]) for i in range(0, len(cur), 2)]
        levels.append(cur)
    return cur[0], levels

def auth_path(levels, idx):
    path = []
    for lvl in levels[:-1]:
        path.append(lvl[idx ^ 1])
        idx >>= 1
    return path

def merkle_root_from_leaf(leaf, idx, path):
    node = leaf
    for sib in path:
        node = H(b"\x01" + (node + sib if idx & 1 == 0 else sib + node))
        idx >>= 1
    return node

class Signer:
    def __init__(self, rng):
        self.sk = [[rng(N) for _ in range(LEN)] for _ in range(1 << TREE_H)]  # per-leaf WOTS sk
        self.leaves = [H(b"\x00" + wots_pk(s)) for s in self.sk]
        self.root, self.levels = merkle(self.leaves)
        self.ctr = 0

    def sign(self, msg, leaf=None):
        q = self.ctr if leaf is None else leaf
        sig = {"leaf": q, "wots": wots_sign(self.sk[q], msg),
               "path": auth_path(self.levels, q)}
        if leaf is None:
            self.ctr += 1
        return sig

def verify(msg, sig, root):
    leaf = H(b"\x00" + wots_pk_from_sig(msg, sig["wots"]))
    return merkle_root_from_leaf(leaf, sig["leaf"], sig["path"]) == root
