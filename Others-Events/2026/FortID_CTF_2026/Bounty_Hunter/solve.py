import hashlib
import json
import os
import sys

P = 35182531786822156541290684230036086178800502148536840364113258180206318266211


def F(x):
    return int(x) % P


def inv(x):
    return pow(F(x), P - 2, P)


def h_int(*parts):
    h = hashlib.sha256()
    for part in parts:
        b = part if isinstance(part, bytes) else str(part).encode()
        h.update(len(b).to_bytes(4, "big"))
        h.update(b)
    return int.from_bytes(h.digest(), "big") % P


def bits_le(x, n):
    return [(int(x) >> i) & 1 for i in range(n)]


def point_bits(report_id, field, manifest):
    enc = manifest["encoding"]
    col = enc["columns"][field]
    return bits_le(report_id, enc["report_id_bits"]) + bits_le(col, enc["column_bits"])


def challenge(snapshot_id, commitment, report_id, field, claimed_value):
    r = h_int("TwinFold-v2", snapshot_id, commitment, report_id, field, claimed_value)
    return 7 if r in (0, 1, P - 1) else r


def ladder(rho, n):
    xs = []
    x = F(rho)
    for _ in range(n + 1):
        xs.append(x)
        x = x * x % P
    return xs


def eval_poly(coeffs, x):
    y = 0
    x = F(x)
    for c in reversed(coeffs):
        y = (y * x + F(c)) % P
    return y


def commit(coeffs):
    h = hashlib.sha256()
    h.update(b"TwinFold coefficient commitment")
    h.update(len(coeffs).to_bytes(4, "big"))
    for c in coeffs:
        h.update(F(c).to_bytes(32, "big"))
    return h.hexdigest()


def fold_value(a, b, bit, x):
    a = F(a)
    b = F(b)
    x = F(x)
    if bit == 0:
        return (a + b) * inv(2) % P
    return (a - b) * inv(2 * x) % P


def load_local_manifest_and_vector():
    with open("manifest.json", "r") as f:
        manifest = json.load(f)

    vector = []
    for i in range(8):
        shard_file = f"{i:03d}.json"
        if not os.path.exists(shard_file):
            print(f"[-] Thiếu file shard: {shard_file}")
            sys.exit(1)
        with open(shard_file, "r") as f:
            data = json.load(f)
            vector.extend([F(x) for x in data["values"]])
    return manifest, vector


def forge_proof():
    manifest, vector = load_local_manifest_and_vector()

    target_field = "payout_authorized"
    target_report_id = 604
    claimed_value = 1

    bits = point_bits(target_report_id, target_field, manifest)
    n = len(bits)  # 13

    rho = challenge(
        manifest["snapshot_id"],
        manifest["commitment"],
        target_report_id,
        target_field,
        claimed_value,
    )
    xs = ladder(rho, n)

    # 1. Tính toán giá trị gập thật tại Round 0
    a0 = eval_poly(vector, xs[0])
    b0 = eval_poly(vector, -xs[0])
    v1 = fold_value(a0, b0, bits[0], xs[0])

    # 2. Đặt mục tiêu cho các giá trị sau gập: v[1] = v1, từ v[2] trở đi ép về 1
    v = [0] * (n + 1)
    v[1] = v1
    for k in range(2, n + 1):
        v[k] = claimed_value

    # 3. Dựng chuỗi đa thức bậc 1 cho next_coeffs của từng round
    next_polynomials = []
    for i in range(n - 1):
        # next_coeffs của round i sẽ là đa thức P_{i+1}(X) được dùng ở round i+1
        bit_next = bits[i + 1]
        x_next = xs[i + 1]
        v_curr = v[i + 1]
        v_next = v[i + 2]

        if bit_next == 0:
            c0 = v_next
            c1 = (v_curr - c0) * inv(x_next) % P
        else:
            c1 = v_next
            c0 = (v_curr - c1 * x_next) % P

        next_polynomials.append([F(c0), F(c1)])

    # Round cuối cùng (Round 12): next_coeffs là hằng số [claimed_value]
    next_polynomials.append([F(claimed_value)])

    # 4. Ráp toàn bộ rounds và fold_commitments
    rounds = []
    fold_commitments = []
    current_coeffs = vector

    for i in range(n):
        ai = eval_poly(current_coeffs, xs[i])
        bi = eval_poly(current_coeffs, -xs[i])
        nxt_c = next_polynomials[i]

        comm = commit(nxt_c)
        fold_commitments.append(comm)

        rounds.append(
            {
                "a": str(ai),
                "b": str(bi),
                "next_coeffs": [str(c) for c in nxt_c],
            }
        )

        current_coeffs = nxt_c

    proof = {
        "claimed_value": str(claimed_value),
        "field": target_field,
        "fold_commitments": fold_commitments,
        "report_id": target_report_id,
        "rounds": rounds,
        "scheme": manifest["scheme"],
        "snapshot_id": manifest["snapshot_id"],
    }

    return proof


if __name__ == "__main__":
    print("[*] Đang sinh forged proof...")
    proof = forge_proof()

    output_filename = "forged_proof.json"
    with open(output_filename, "w") as f:
        json.dump(proof, f, indent=2)

    print(f"[+] Đã tạo thành công {output_filename}!")

    # Tự kiểm tra lại bằng chính logic verifier.py
    if os.path.exists("verifier.py"):
        import verifier

        manifest, vector = load_local_manifest_and_vector()
        ok, msg = verifier.verify(proof, manifest, vector)
        print(f"[*] Verifier test: {msg} (Valid: {ok})")
        reports = {"vault_policy": manifest["vault_policy"]}
        print(
            "[*] Vault policy check:",
            "PASSED" if verifier.vault_policy(proof, reports) else "FAILED",
        )