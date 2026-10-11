import argparse
import hashlib
import json
import urllib.request

P = 35182531786822156541290684230036086178800502148536840364113258180206318266211


def F(x):
    return int(x) % P


def inv(x):
    return pow(F(x), P - 2, P)


def load(path):
    if path.startswith("http://") or path.startswith("https://"):
        with urllib.request.urlopen(path) as r:
            return json.loads(r.read().decode())
    with open(path, "r") as f:
        return json.load(f)


def fetch(base, path):
    return load(base.rstrip("/") + path)


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


def cell_index(report_id, field, manifest):
    return sum(b << i for i, b in enumerate(point_bits(report_id, field, manifest)))


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


def load_vector(base, manifest):
    out = []
    for shard in manifest["shards"]:
        data = fetch(base, shard["path"])
        out += [F(x) for x in data["values"]]
    return out


def verify(proof, manifest, vector):
    if proof["scheme"] != manifest["scheme"]:
        return False, "wrong scheme"
    if proof["snapshot_id"] != manifest["snapshot_id"]:
        return False, "wrong snapshot"
    if proof["field"] not in manifest["encoding"]["columns"]:
        return False, "unknown field"

    report_id = int(proof["report_id"])
    claimed = F(proof["claimed_value"])
    bits = point_bits(report_id, proof["field"], manifest)
    n = len(bits)

    if len(proof["rounds"]) != n:
        return False, "wrong number of rounds"
    if len(proof["fold_commitments"]) != n:
        return False, "wrong number of commitments"

    rho = challenge(manifest["snapshot_id"], manifest["commitment"], report_id, proof["field"], claimed)
    xs = ladder(rho, n)
    coeffs = [F(x) for x in vector]

    for i in range(n):
        if commit(coeffs) != (manifest["commitment"] if i == 0 else proof["fold_commitments"][i - 1]):
            return False, f"bad commitment in round {i}"

        r = proof["rounds"][i]
        a = eval_poly(coeffs, xs[i])
        b = eval_poly(coeffs, -xs[i])

        if a != F(r["a"]):
            return False, f"bad +x evaluation in round {i}"
        if b != F(r["b"]):
            return False, f"bad -x evaluation in round {i}"

        next_coeffs = [F(x) for x in r["next_coeffs"]]
        if len(next_coeffs) == 0:
            return False, f"empty next polynomial in round {i}"
        if commit(next_coeffs) != proof["fold_commitments"][i]:
            return False, f"bad next commitment in round {i}"

        next_value = claimed if i == n - 1 else F(proof["rounds"][i + 1]["a"])
        if fold_value(a, b, bits[i], xs[i]) != next_value:
            return False, f"fold equation failed in round {i}"

        coeffs = next_coeffs

    if eval_poly(coeffs, xs[-1]) != claimed:
        return False, "bad final evaluation"

    return True, "accepted"


def vault_policy(proof, reports):
    policy = reports["vault_policy"]
    return (
        int(proof["report_id"]) in set(map(int, policy["owned_report_ids"]))
        and proof["field"] == policy["field"]
        and str(proof["claimed_value"]) == str(policy["required_claimed_value"])
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("proof")
    args = ap.parse_args()

    base = args.base.rstrip("/")
    proof = load(args.proof)
    manifest = fetch(base, "/api/transparency/snapshots/latest/manifest.json")
    reports = fetch(base, "/api/reports.json")
    vector = load_vector(base, manifest)

    ok, msg = verify(proof, manifest, vector)
    print(msg)
    if ok:
        print(f"claim: {proof['field']}({proof['report_id']}) = {proof['claimed_value']}")
        print("payout:", "yes" if vault_policy(proof, reports) else "no")


if __name__ == "__main__":
    main()
