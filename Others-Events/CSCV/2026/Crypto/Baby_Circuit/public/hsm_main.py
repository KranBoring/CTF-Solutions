#!/usr/bin/env python3
import os, json, socketserver, secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from plonk_engine import (
    KZGSetup, CircuitSelectors, build_proof, hardware_specs,
    check_envelope, QUERY_BUDGET, CIRCUIT_ROWS, GATE_FORMS, DOMAIN_SIZE
)
import hw_model

SESSION_TIMEOUT = 90
FLAG = b"FLAG{test_oracle_local__real_flag_is_online}"


class Session:
    def __init__(self):
        self.ready = False
        self.queries = 0
        self.h = None

    def ensure(self):
        if self.ready:
            return
        self.h = hw_model.new_session()
        pub = hw_model.session_public(self.h)
        self.pub = pub
        self.p = int(pub["field_prime"], 16)
        self.mds = hw_model.session_mds(self.h)
        self.rc = hw_model.session_round_constants(self.h)
        self.kzg = KZGSetup(p_mod=self.p)
        self.sel = CircuitSelectors(self.mds, self.rc[0],
                                    int(pub["shear_alpha1"], 16),
                                    int(pub["shear_alpha2"], 16),
                                    int(pub["shear_alpha3"], 16),
                                    self.p)
        key = hw_model.session_key(self.h)
        self.iv = secrets.token_bytes(16)
        self.enc = AES.new(key, AES.MODE_CBC, self.iv).encrypt(pad(FLAG, 16)).hex()
        self.ready = True

    def close(self):
        if self.h is not None:
            hw_model.close_session(self.h)
            self.h = None

    def handle(self, req):
        a = req.get("action", "")
        if a == "get_hardware_specs":
            self.ensure()
            return {"status": "success",
                    "hardware_specs": hardware_specs(),
                    "circuit": {
                        "domain_size": DOMAIN_SIZE,
                        "rows": {str(r): {"gate": g, "lane": l}
                                 for r, (g, l) in sorted(CIRCUIT_ROWS.items())},
                        "gate_forms": dict(GATE_FORMS),
                        "accumulator": {"column": "a", "rows": "0 .. n-2",
                                        "form": "z(omega*X) - z(X) - a(X) = 0",
                                        "note": "running-sum witness checksum over column a; "
                                                "z(w^0) = 0 and the wrap row n-1 is excluded"}},
                    "poseidon_mds": [[hex(x) for x in row] for row in self.mds],
                    "round_constants": [[hex(x) for x in row] for row in self.rc],
                    "session_parameters": self.pub,
                    "iv": self.iv.hex(), "encrypted_flag": self.enc}
        if a == "prove":
            self.ensure()
            x1 = int(req.get("public_nonce", "0x1234"), 16) % self.p
            x2 = int(req.get("public_nonce2", "0x5678"), 16) % self.p
            v = int(req.get("core_voltage_mv", 1200))
            f = int(req.get("clock_freq_mhz", 80))
            try:
                check_envelope(v, f)
                if self.queries >= QUERY_BUDGET:
                    return {"status": "error",
                            "message": f"Query budget of {QUERY_BUDGET} proofs exceeded."}
                cols = hw_model.build_columns(self.h, x1, x2, v, f)
                pf = build_proof(self.kzg, self.sel, cols["a"], cols["b"], cols["c"],
                                 x1, cols["hash"])
                self.queries += 1
                return {"status": "success", "proof": pf,
                        "applied_voltage_mv": v, "applied_freq_mhz": f,
                        "queries_remaining": QUERY_BUDGET - self.queries}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        return {"status": "error", "message": f"Unknown action: {a}"}


class Handler(socketserver.StreamRequestHandler):
    timeout = SESSION_TIMEOUT

    def handle(self):
        sess = Session()
        self.wfile.write((json.dumps({
            "banner": "=== SECURE 32-ROUND ZK-SNARK HARDWARE ACCELERATOR HSM (PROPRIETARY) ===",
            "session_lifetime_seconds": SESSION_TIMEOUT,
            "query_budget": QUERY_BUDGET,
            "supported_actions": ["get_hardware_specs", "prove"],
            "note": "Offline oracle, TEST flag only. Recover the key, decrypt, get the test "
                    "flag; run your finished solver against the online instance for the real "
                    "one."}) + "\n").encode())
        try:
            while True:
                line = self.rfile.readline()
                if not line:
                    break
                try:
                    req = json.loads(line.decode().strip())
                except Exception:
                    self.wfile.write(b'{"status":"error","message":"bad json"}\n')
                    continue
                self.wfile.write((json.dumps(sess.handle(req)) + "\n").encode())
        except Exception:
            pass
        finally:
            sess.close()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    host = os.environ.get("HSM_HOST", "0.0.0.0")
    port = int(os.environ.get("HSM_PORT", "1337"))
    print(f"[*] HSM offline oracle (TEST flag) on {host}:{port}", flush=True)
    Server((host, port), Handler).serve_forever()
