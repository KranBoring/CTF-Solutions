#!/usr/bin/env python3
"""
Challenge: Quantum Echo (h4ckc0n 2026)
Category: Crypto / Algebraic Attack over GF(2)
Solver: SageMath
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct

from sage.all import GF, Matrix, vector


def rotl(x: int, n: int, bits: int = 32) -> int:
    """Cyclic left rotation của số nguyên 32-bit."""
    n %= bits
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)


def calibrate_rotations(probes: list[dict]) -> tuple[int, int, int]:
    """Tự động tìm hằng số quay bit từ các mẫu hiệu chuẩn (calibration probes)."""
    # 1. Walk rotation: walk_word = rotl(input, k)
    walk_k = next(
        k for k in range(32)
        if all(rotl(int(p["input"], 16), k) == int(p["walk_word"], 16) for p in probes)
    )

    # 2. Fold rotations: fold_word = input ^ (rotl(input, r1) & rotl(input, r2))
    fold_r1, fold_r2 = next(
        (r1, r2)
        for r1 in range(32)
        for r2 in range(r1 + 1, 32)
        if all(
            int(p["input"], 16) ^ (rotl(int(p["input"], 16), r1) & rotl(int(p["input"], 16), r2))
            == int(p["fold_word"], 16)
            for p in probes
        )
    )

    return walk_k, fold_r1, fold_r2


def main() -> None:
    chal_path = Path(__file__).parent / "challenge.json"
    with open(chal_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Bước 1: Hiệu chuẩn hằng số quay
    probes = data["register"]["controller_calibration"]["probes"]
    walk_k, fold_r1, fold_r2 = calibrate_rotations(probes)
    print(f"[*] Calibration: walk_k={walk_k}, fold_r1={fold_r1}, fold_r2={fold_r2}")

    # Bước 2: Dựng ma trận hệ phương trình tuyến tính trên GF(2)
    # 81 biến nhị phân:
    #   0..31  : fold_mask (s)
    #   32..63 : walk_mask (t)
    #   64     : e0
    #   65..80 : q_0 .. q_15 (chân tiếp xúc A..P)
    num_vars = 81
    rows: list[list[int]] = []
    rhs: list[int] = []
    accum_walk = 0

    for i, obs in enumerate(data["register"]["observations"]):
        x, z = obs["x"], obs["z"]
        fold_word = x ^ (rotl(x, fold_r1) & rotl(x, fold_r2))
        walk_word = rotl(x, walk_k)
        accum_walk ^= walk_word

        row = [0] * num_vars
        for b in range(32):
            if (fold_word >> b) & 1:
                row[b] = 1
            if (accum_walk >> b) & 1:
                row[32 + b] = 1

        row[64] = 1              # e0
        row[65 + (i % 16)] = 1   # pad bit q (tuần hoàn 16 chân A..P)

        rows.append(row)
        rhs.append(z)

    # Ràng buộc từ quantum_transcript: sample 0 contact A -> q_0 = 1
    row_q0 = [0] * num_vars
    row_q0[65] = 1
    rows.append(row_q0)
    rhs.append(1)

    # Bước 3: Giải hệ tuyến tính cực gọn bằng SageMath Matrix trên GF(2)
    M = Matrix(GF(2), rows)
    b = vector(GF(2), rhs)
    sol = M.solve_right(b)

    fold_mask = sum(int(sol[b]) << b for b in range(32))
    walk_mask = sum(int(sol[32 + b]) << b for b in range(32))
    e0 = int(sol[64])
    q_bits = "".join(str(int(sol[65 + k])) for k in range(16))

    print(f"[*] Recovered s (fold_mask): {fold_mask:08x}")
    print(f"[*] Recovered t (walk_mask): {walk_mask:08x}")
    print(f"[*] Recovered e0           : {e0}")
    print(f"[*] Recovered q (pad_bits) : {q_bits}")

    # Bước 4: Tạo material và giải mã flag bằng SHA-256 keystream
    material = f"{fold_mask:08x}:{walk_mask:08x}:{e0}:{q_bits}".encode("ascii")
    sealed_flag = bytes.fromhex(data["sealed_flag"])

    keystream = bytearray()
    counter = 0
    while len(keystream) < len(sealed_flag):
        keystream.extend(hashlib.sha256(material + struct.pack(">I", counter)).digest())
        counter += 1

    flag = bytes(c ^ k for c, k in zip(sealed_flag, keystream[: len(sealed_flag)]))
    print(f"\n[+] Flag: {flag.decode('utf-8', errors='replace')}")


if __name__ == "__main__":
    main()
