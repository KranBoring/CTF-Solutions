#!/usr/bin/env python3
import secrets
import hashlib
from typing import List, Tuple, Dict, Any

DEFAULT_P = 21888242871839275222246405745257275088548364400416034343698204186575808495617
p = DEFAULT_P

q = 21888242871839275222246405745257275088696311157297823662689037894645226208583
G1 = (1, 2)


def to_jacobian(P):
    if P is None:
        return (1, 1, 0)
    return (P[0], P[1], 1)


def from_jacobian(J):
    X, Y, Z = J
    if Z == 0:
        return None
    z_inv = pow(Z, q - 2, q)
    z_inv2 = (z_inv * z_inv) % q
    z_inv3 = (z_inv2 * z_inv) % q
    return ((X * z_inv2) % q, (Y * z_inv3) % q)


def jacobian_double(J):
    X1, Y1, Z1 = J
    if Z1 == 0 or Y1 == 0:
        return (1, 1, 0)
    A = (X1 * X1) % q
    B = (Y1 * Y1) % q
    C = (B * B) % q
    D = (2 * ((X1 + B) * (X1 + B) - A - C)) % q
    E = (3 * A) % q
    F = (E * E) % q
    X3 = (F - 2 * D) % q
    Y3 = (E * (D - X3) - 8 * C) % q
    Z3 = (2 * Y1 * Z1) % q
    return (X3, Y3, Z3)


def jacobian_add(J1, J2):
    X1, Y1, Z1 = J1
    X2, Y2, Z2 = J2
    if Z1 == 0:
        return J2
    if Z2 == 0:
        return J1
    Z1Z1 = (Z1 * Z1) % q
    Z2Z2 = (Z2 * Z2) % q
    U1 = (X1 * Z2Z2) % q
    U2 = (X2 * Z1Z1) % q
    S1 = (Y1 * Z2 * Z2Z2) % q
    S2 = (Y2 * Z1 * Z1Z1) % q
    if U1 == U2:
        if S1 != S2:
            return (1, 1, 0)
        return jacobian_double(J1)
    H = (U2 - U1) % q
    I = (4 * H * H) % q
    J = (H * I) % q
    r = (2 * (S2 - S1)) % q
    V = (U1 * I) % q
    X3 = (r * r - J - 2 * V) % q
    Y3 = (r * (V - X3) - 2 * S1 * J) % q
    Z3 = (((Z1 + Z2) * (Z1 + Z2) - Z1Z1 - Z2Z2) * H) % q
    return (X3, Y3, Z3)


def point_mul(P, scalar, p_order: int = DEFAULT_P):
    scalar = scalar % p_order
    if scalar == 0 or P is None:
        return None
    curr = to_jacobian(P)
    res = (1, 1, 0)
    while scalar > 0:
        if scalar & 1:
            res = jacobian_add(res, curr)
        curr = jacobian_double(curr)
        scalar >>= 1
    return from_jacobian(res)


def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    return from_jacobian(jacobian_add(to_jacobian(P), to_jacobian(Q)))


def poly_add(a: List[int], b: List[int], p_mod: int = DEFAULT_P) -> List[int]:
    length = max(len(a), len(b))
    res = [0] * length
    for i in range(length):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        res[i] = (ai + bi) % p_mod
    return trim_poly(res)


def poly_mul(a: List[int], b: List[int], p_mod: int = DEFAULT_P) -> List[int]:
    if not a or not b:
        return [0]
    res = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if not ca:
            continue
        for j, cb in enumerate(b):
            res[i + j] = (res[i + j] + ca * cb) % p_mod
    return trim_poly(res)


def poly_eval(poly: List[int], x: int, p_mod: int = DEFAULT_P) -> int:
    res = 0
    for c in reversed(poly):
        res = (res * x + c) % p_mod
    return res


def trim_poly(p_poly: List[int]) -> List[int]:
    while len(p_poly) > 1 and p_poly[-1] == 0:
        p_poly.pop()
    return p_poly


def poly_div(a: List[int], b: List[int], p_mod: int = DEFAULT_P) -> Tuple[List[int], List[int]]:
    a = a[:]
    b = trim_poly(b[:])
    if len(b) == 1 and b[0] == 0:
        raise ZeroDivisionError("Polynomial division by zero")
    quotient = [0] * max(1, len(a) - len(b) + 1)
    inv_lead_b = pow(b[-1], p_mod - 2, p_mod)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        deg_diff = len(a) - len(b)
        factor = (a[-1] * inv_lead_b) % p_mod
        quotient[deg_diff] = factor
        for i in range(len(b)):
            a[deg_diff + i] = (a[deg_diff + i] - factor * b[i]) % p_mod
        a = trim_poly(a)
    return trim_poly(quotient), trim_poly(a)


def poly_div_by_linear(poly: List[int], root: int, p_mod: int = DEFAULT_P) -> List[int]:
    d = len(poly) - 1
    if d <= 0:
        return [0]
    q_poly = [0] * d
    q_poly[d - 1] = poly[d]
    for i in range(d - 2, -1, -1):
        q_poly[i] = (poly[i + 1] + root * q_poly[i + 1]) % p_mod
    return trim_poly(q_poly)


DOMAIN_SIZE = 64


def find_generator_and_omega(p_mod: int, n: int = DOMAIN_SIZE) -> Tuple[int, int]:
    g = 2
    while pow(g, (p_mod - 1) // 2, p_mod) == 1:
        g += 1
    return g, pow(g, (p_mod - 1) // n, p_mod)


def interpolate_domain(values: List[int], p_mod: int = DEFAULT_P, omega: int = None) -> List[int]:
    if omega is None:
        _, omega = find_generator_and_omega(p_mod, DOMAIN_SIZE)
    inv_omega = pow(omega, p_mod - 2, p_mod)
    inv_n = pow(DOMAIN_SIZE, p_mod - 2, p_mod)
    coeffs = [0] * DOMAIN_SIZE
    for j in range(DOMAIN_SIZE):
        s = 0
        w_j = pow(inv_omega, j, p_mod)
        w_power = 1
        for k in range(DOMAIN_SIZE):
            s = (s + values[k] * w_power) % p_mod
            w_power = (w_power * w_j) % p_mod
        coeffs[j] = (s * inv_n) % p_mod
    return trim_poly(coeffs)


class KZGSetup:
    def __init__(self, p_mod: int = DEFAULT_P, max_degree: int = 200):
        self.p = p_mod
        self.tau = 0x1337c0ffeebabe123456789abcdef0123456789abcdef % self.p
        self.srs_g1 = [point_mul(G1, pow(self.tau, i, self.p), self.p) for i in range(max_degree + 1)]

    def commit(self, poly: List[int]) -> Tuple[int, int]:
        res = None
        for i, coeff in enumerate(poly):
            if coeff % self.p != 0 and i < len(self.srs_g1):
                res = point_add(res, point_mul(self.srs_g1[i], coeff % self.p, self.p))
        return res if res is not None else (0, 0)

    def open(self, poly: List[int], point: int) -> Tuple[int, Tuple[int, int]]:
        eval_val = poly_eval(poly, point, self.p)
        return eval_val, self.commit(poly_div_by_linear(poly, point, self.p))


# ------------------------------------------------------------- timing model
BASE_DELAY_NS = 6.0
NOMINAL_COEFFS = {
    "stage_a": 1.50,
    "stage_b": 0.50,
    "stage_c": 0.50,
    "stage_d": 0.60,
    "stage_e": 1.85,
    "stage_f": 1.70,
}
STAGE_NAMES = list(NOMINAL_COEFFS)
MAX_FREQ_MHZ = 133
MIN_VOLTAGE_MV = 1000
QUERY_BUDGET = 2

STATE_WIDTH = 4
LINEAR_BITS = 96
LOAD_BITS = 54


def hardware_specs() -> Dict[str, Any]:
    return {
        "device_name": "ZK-SNARK Hardware Cryptographic Accelerator v4.1 (Proprietary)",
        "nominal_voltage_mv": 1200,
        "nominal_freq_mhz": 80,
        "max_operating_freq_mhz": MAX_FREQ_MHZ,
        "min_core_voltage_mv": MIN_VOLTAGE_MV,
        "sponge": {
            "state_width": STATE_WIDTH,
            "sbox": "x^5",
            "partial_rounds": "r = 0 .. 23 (S-box on lane 0 only)",
            "full_rounds": "r = 24 .. 31 (S-box on all four lanes)",
            "round": "s[r+1] = M . y[r] + rc[r]",
            "state_load": "s0 = ( load(r1, r2), w, public_nonce, public_nonce2 )",
            "output": "s32[0]"
        },
        "timing_model": {
            "base_delay_ns": BASE_DELAY_NS,
            "stage_delay_coefficients": dict(NOMINAL_COEFFS),
            "formula": "T_delay(V, stage) = base_delay_ns * (1200 / V)^2 * stage_coeff[stage]",
            "clock_period_ns": "T_clk(F) = 1000 / F",
            "latching": "a stage output register latches correctly while T_delay <= T_clk, and "
                        "reads 0 for the rest of that run once T_delay > T_clk; the mapping from "
                        "pipeline stages to datapath registers is not published"
        },
        "bist_unit": {
            "note": "a two-stage built-in self-test comparator samples the datapath at the "
                    "round-24 macro-stage boundary and is constrained in the circuit through "
                    "the shear gates; its trim coefficients were fixed at manufacturing and "
                    "are the published shear selectors"
        },
        "key_registers": {
            "count": 3,
            "widths_bits": [LINEAR_BITS, LOAD_BITS, LOAD_BITS],
            "note": "three master-key registers w, r1, r2. w is loaded straight into lane 1 of "
                    "the sponge state. r1 and r2 are never loaded directly; they reach the "
                    "datapath only through the lane-0 load "
                    "load(r1, r2) = r1^2 + A*r1*r2 + B*r2^2 + C*r1 + D*r2 + E (mod p), whose "
                    "coefficients are published as session_parameters.load_coeffs. "
                    "AES-256 key = SHA256(w || r1 || r2), each register 32 bytes big-endian"
        },
        "query_budget": QUERY_BUDGET
    }


def check_envelope(core_voltage_mv: int, clock_freq_mhz: int):
    if clock_freq_mhz > MAX_FREQ_MHZ or core_voltage_mv < MIN_VOLTAGE_MV:
        raise ValueError(
            "Hardware Protection Triggered: clock exceeds PLL operating limit "
            f"({MAX_FREQ_MHZ} MHz) or core voltage below {MIN_VOLTAGE_MV} mV."
        )


def stage_margins(core_voltage_mv: int, clock_freq_mhz: int, coeffs: Dict[str, float]) -> Dict[str, float]:
    t_clk = 1000.0 / max(1, clock_freq_mhz)
    scale = (1200.0 / max(1, core_voltage_mv)) ** 2
    return {name: t_clk - BASE_DELAY_NS * scale * coeffs[name] for name in STAGE_NAMES}


def evaluate_timing_violations(core_voltage_mv: int, clock_freq_mhz: int) -> Dict[str, bool]:
    check_envelope(core_voltage_mv, clock_freq_mhz)
    return {n: m < 0 for n, m in stage_margins(core_voltage_mv, clock_freq_mhz, NOMINAL_COEFFS).items()}


# ------------------------------------------------------- sponge specification
NUM_ROUNDS = 32
NUM_PARTIAL_ROUNDS = 24


def poseidon_round(s: List[int], rc_row: List[int], is_full: bool, p_mod: int,
                   mds: List[List[int]]) -> Tuple[List[int], List[int]]:
    if is_full:
        y = [pow(v, 5, p_mod) for v in s]
    else:
        y = [pow(s[0], 5, p_mod)] + list(s[1:])
    s_next = [(sum(mds[i][j] * y[j] for j in range(STATE_WIDTH)) + rc_row[i]) % p_mod
              for i in range(STATE_WIDTH)]
    return y, s_next


def poseidon_hash(s0: List[int], rc: List[List[int]], mds: List[List[int]], p_mod: int) -> int:
    s = s0[:]
    for r in range(NUM_ROUNDS):
        _, s = poseidon_round(s, rc[r], r >= NUM_PARTIAL_ROUNDS, p_mod, mds)
    return s[0]


# ------------------------------------------------------------------- circuit
CIRCUIT_ROWS = {
    3:  ("mul", None),
    7:  ("lin", 0),
    12: ("pass", None),
    17: ("lin", 1),
    22: ("mul", None),
    26: ("pass", None),
    31: ("lin", 2),
    35: ("mul", None),
    40: ("shear3", None),
    44: ("lin", 3),
    49: ("mul", None),
    53: ("pass", None),
    57: ("mul", None),
    60: ("shear", None),
}

ACC_COLUMN = "a"

GATE_FORMS = {
    "mul": "a*b - c = 0",
    "pass": "a - c = 0",
    "sub": "a - b - c = 0",
    "add": "a + b - c = 0",
    "shear": "alpha1*a + alpha2*b - c = 0",
    "shear3": "a + alpha3*b - c = 0",
    "lin": "M[lane][0]*a + M[lane][1]*b - c + rc0[lane] = 0",
}


def gate_selectors(gate_type: str, lane, mds: List[List[int]], rc0: List[int],
                   alpha1: int, alpha2: int, alpha3: int, p_mod: int):
    if gate_type == "mul":
        return (1, 0, 0, -1, 0)
    if gate_type == "pass":
        return (0, 1, 0, -1, 0)
    if gate_type == "sub":
        return (0, 1, -1, -1, 0)
    if gate_type == "add":
        return (0, 1, 1, -1, 0)
    if gate_type == "shear":
        return (0, alpha1, alpha2, -1, 0)
    if gate_type == "shear3":
        return (0, 1, alpha3, -1, 0)
    if gate_type == "lin":
        return (0, mds[lane][0], mds[lane][1], -1, rc0[lane])
    raise ValueError(gate_type)


class CircuitSelectors:
    def __init__(self, mds: List[List[int]], rc0: List[int], alpha1: int, alpha2: int,
                 alpha3: int, p_mod: int = DEFAULT_P):
        self.p = p_mod
        self.n = DOMAIN_SIZE
        _, self.omega = find_generator_and_omega(self.p, self.n)
        self.z_h = [-1] + [0] * (self.n - 1) + [1]
        cols = [[0] * self.n for _ in range(6)]
        for row, (gtype, lane) in CIRCUIT_ROWS.items():
            qs = gate_selectors(gtype, lane, mds, rc0, alpha1, alpha2, alpha3, self.p)
            for k in range(5):
                cols[k][row] = qs[k] % self.p
        for row in range(self.n - 1):
            cols[5][row] = 1
        self.q_M, self.q_L, self.q_R, self.q_O, self.q_C, self.q_acc = (
            interpolate_domain(col, p_mod=self.p, omega=self.omega) for col in cols)


def shift_by_omega(poly: List[int], omega: int, p_mod: int) -> List[int]:
    return [(cf * pow(omega, k, p_mod)) % p_mod for k, cf in enumerate(poly)]


def build_proof(kzg: KZGSetup, sel: CircuitSelectors, a_vals: List[int], b_vals: List[int],
                c_vals: List[int], x_pub: int, final_hash: int) -> Dict[str, Any]:
    p_mod = sel.p
    w_a_raw = interpolate_domain(a_vals, p_mod=p_mod, omega=sel.omega)
    w_b_raw = interpolate_domain(b_vals, p_mod=p_mod, omega=sel.omega)
    w_c_raw = interpolate_domain(c_vals, p_mod=p_mod, omega=sel.omega)

    b1, b2, b3 = secrets.randbelow(p_mod), secrets.randbelow(p_mod), secrets.randbelow(p_mod)
    w_a = poly_add(w_a_raw, poly_mul([b1], sel.z_h, p_mod), p_mod)
    w_b = poly_add(w_b_raw, poly_mul([b2], sel.z_h, p_mod), p_mod)
    w_c = poly_add(w_c_raw, poly_mul([b3], sel.z_h, p_mod), p_mod)

    cm_a = kzg.commit(w_a)
    cm_b = kzg.commit(w_b)
    cm_c = kzg.commit(w_c)

    acc = [0] * sel.n
    for i in range(sel.n - 1):
        acc[i + 1] = (acc[i] + a_vals[i]) % p_mod
    z_raw = interpolate_domain(acc, p_mod=p_mod, omega=sel.omega)

    b4, b5 = secrets.randbelow(p_mod), secrets.randbelow(p_mod)
    z_poly = poly_add(z_raw, poly_mul([b4, b5], sel.z_h, p_mod), p_mod)
    cm_z = kzg.commit(z_poly)

    transcript_bytes = f"{cm_a}{cm_b}{cm_c}{cm_z}{x_pub}{final_hash}".encode()
    zeta = int(hashlib.sha256(transcript_bytes).hexdigest(), 16) % p_mod
    zeta_omega = (zeta * sel.omega) % p_mod

    z_shift = shift_by_omega(z_poly, sel.omega, p_mod)
    acc_diff = poly_add(z_shift, [(-v) % p_mod for v in poly_add(z_poly, w_a, p_mod)], p_mod)
    term_M = poly_mul(sel.q_M, poly_mul(w_a, w_b, p_mod), p_mod)
    term_L = poly_mul(sel.q_L, w_a, p_mod)
    term_R = poly_mul(sel.q_R, w_b, p_mod)
    term_O = poly_mul(sel.q_O, w_c, p_mod)
    term_A = poly_mul(sel.q_acc, acc_diff, p_mod)
    f_gate = sel.q_C
    for term in (term_M, term_L, term_R, term_O, term_A):
        f_gate = poly_add(f_gate, term, p_mod)

    t_poly = poly_div(f_gate, sel.z_h, p_mod)[0]
    cm_t = kzg.commit(t_poly)

    eval_a, proof_a = kzg.open(w_a, zeta)
    eval_b, proof_b = kzg.open(w_b, zeta)
    eval_c, proof_c = kzg.open(w_c, zeta)
    eval_z, proof_z = kzg.open(z_poly, zeta)
    eval_zw, proof_zw = kzg.open(z_poly, zeta_omega)
    eval_t, proof_t = kzg.open(t_poly, zeta)

    return {
        "commitments": {
            "cm_a": [hex(cm_a[0]), hex(cm_a[1])],
            "cm_b": [hex(cm_b[0]), hex(cm_b[1])],
            "cm_c": [hex(cm_c[0]), hex(cm_c[1])],
            "cm_z": [hex(cm_z[0]), hex(cm_z[1])],
            "cm_t": [hex(cm_t[0]), hex(cm_t[1])]
        },
        "zeta": hex(zeta),
        "evaluations": {
            "eval_a": hex(eval_a),
            "eval_b": hex(eval_b),
            "eval_c": hex(eval_c),
            "eval_z": hex(eval_z),
            "eval_z_omega": hex(eval_zw),
            "eval_t": hex(eval_t)
        },
        "kzg_proofs": {
            "proof_a": [hex(proof_a[0]), hex(proof_a[1])],
            "proof_b": [hex(proof_b[0]), hex(proof_b[1])],
            "proof_c": [hex(proof_c[0]), hex(proof_c[1])],
            "proof_z": [hex(proof_z[0]), hex(proof_z[1])],
            "proof_z_omega": [hex(proof_zw[0]), hex(proof_zw[1])],
            "proof_t": [hex(proof_t[0]), hex(proof_t[1])]
        },
        "public_hash": hex(final_hash)
    }
