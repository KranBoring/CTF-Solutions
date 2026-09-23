#!/usr/bin/env python3
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "flag.txt"), "r", encoding="utf-8") as f:
    FLAG = f.read().strip()


def dsha256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def leaf_hash(item: bytes) -> bytes:
    return dsha256(item)


def node_hash(left: bytes, right: bytes) -> bytes:
    return dsha256(left + right)


def merkle_computation(leaves: list[bytes]) -> bytes:
    if len(leaves) == 0:
        return b"\x00" * 32
    count = 0
    inner = [None] * 32
    while count < len(leaves):
        h = leaves[count]
        count += 1
        level = 0
        while not (count & (1 << level)):
            h = dsha256(inner[level] + h)
            level += 1
        inner[level] = h
    level = 0
    while not (count & (1 << level)):
        level += 1
    h = inner[level]
    while count != (1 << level):
        h = dsha256(h + h)
        count += 1 << level
        level += 1
        while not (count & (1 << level)):
            h = dsha256(inner[level] + h)
            level += 1
    return h


def verify_proof(item: bytes, proof: list, root: bytes) -> bool:
    h = leaf_hash(item)
    for sib, is_left in proof:
        h = node_hash(sib, h) if is_left else node_hash(h, sib)
    return h == root


def parse_proof(raw: str) -> list:
    raw = raw.strip()
    if not raw:
        return []
    out = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError("Invalid proof pair format. Use <hash>:L or <hash>:R")
        h, d = part.split(":", 1)
        sibling = bytes.fromhex(h.strip())
        direction = d.strip().upper()
        if len(sibling) != 32:
            raise ValueError("Proof hashes must be 32 bytes")
        if direction not in {"L", "R"}:
            raise ValueError("Proof direction must be L or R")
        out.append((sibling, direction == "L"))
    return out


def main():
    sys.stdout.reconfigure(line_buffering=True)

    n = random.choice([n for n in range(100, 1001, 4) if (n & (n - 1)) != 0])

    print(f"[+] Number of leaf nodes: {n}")

    items = [os.urandom(32) for _ in range(n)]

    print("\n[+] Public Items:")
    print(json.dumps([itm.hex() for itm in items]))
    print("General form:",items[n-1])
    print("Hex form:",items[n-1].hex())

    leaves = [leaf_hash(x) for x in items]
    root = merkle_computation(leaves)
    print(f"\n[*] Computed Merkle Root(hex form): {root.hex()}")
    print("General form:",root)

    try:
        idx_input = input(f"\nChoose target item index (0 to {n-1}): ").strip()
        target_idx = int(idx_input)
        if target_idx < 0 or target_idx >= n:
            print("[-] Error: Index out of range!")
            return
    except Exception:
        print("[-] Error: Invalid index format!")
        return

    target_item = items[target_idx]

    print("\nSubmit two DIFFERENT valid Merkle proofs for your target item.")
    print("Format: <hash1>:L,<hash2>:R,...")

    try:
        raw_proof_a = input("Proof A: ").strip()
        raw_proof_b = input("Proof B: ").strip()

        proofA = parse_proof(raw_proof_a)
        proofB = parse_proof(raw_proof_b)
    except Exception as e:
        print(f"[-] Parsing Error: {e}")
        return

    if proofA == proofB:
        print("[-] Failed: Proof A and Proof B must be DIFFERENT!")
        return

    if verify_proof(target_item, proofA, root) and verify_proof(target_item, proofB, root):
        print(f"[+] FLAG: {FLAG}")
    else:
        print(f"[-] Verification Failed!")
        print(verify_proof(target_item, proofA, root))
        print(verify_proof(target_item, proofB, root))


if __name__ == "__main__":
    main()
