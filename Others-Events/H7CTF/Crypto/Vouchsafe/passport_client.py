import os
import sys
import json
import base64
import hashlib
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def cbor_head(major, n):
    m = major << 5
    if n < 24:
        return bytes([m | n])
    if n < 0x100:
        return bytes([m | 24, n])
    if n < 0x10000:
        return bytes([m | 25, n >> 8, n & 0xFF])
    if n < 0x100000000:
        return bytes([m | 26, (n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF])
    raise ValueError("too big")


def cbor(obj):
    if isinstance(obj, bool):
        raise ValueError("bool unsupported")
    if isinstance(obj, int):
        return cbor_head(0, obj) if obj >= 0 else cbor_head(1, -1 - obj)
    if isinstance(obj, bytes):
        return cbor_head(2, len(obj)) + obj
    if isinstance(obj, str):
        e = obj.encode()
        return cbor_head(3, len(e)) + e
    if isinstance(obj, list):
        out = cbor_head(4, len(obj))
        for x in obj:
            out += cbor(x)
        return out
    if isinstance(obj, dict):
        out = cbor_head(5, len(obj))
        for k, v in obj.items():
            out += cbor(k) + cbor(v)
        return out
    raise ValueError("unsupported")


def cose_ec2(pub):
    n = pub.public_numbers()
    return {1: 2, 3: -7, -1: 1, -2: n.x.to_bytes(32, "big"), -3: n.y.to_bytes(32, "big")}


def build_auth_data(rp_id, flags, aaguid, cred_id, cose):
    rp_hash = hashlib.sha256(rp_id.encode()).digest()
    out = rp_hash + bytes([flags]) + b"\x00\x00\x00\x00"
    out += aaguid + len(cred_id).to_bytes(2, "big") + cred_id + cbor(cose)
    return out


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    s = requests.Session()

    begin = s.get(base + "/register/begin").json()
    rp_id, origin = begin["rpId"], begin["origin"]
    challenge = base64.urlsafe_b64decode(begin["challenge"] + "==")

    key = ec.generate_private_key(ec.SECP256R1())
    cred_id = os.urandom(16)
    cose = cose_ec2(key.public_key())

    client_data = json.dumps({
        "type": "webauthn.create",
        "challenge": b64u(challenge),
        "origin": origin,
    }, separators=(",", ":")).encode()
    client_hash = hashlib.sha256(client_data).digest()

    flags = 0x01 | 0x04 | 0x40
    auth_data = build_auth_data(rp_id, flags, b"\x00" * 16, cred_id, cose)

    signature = key.sign(auth_data + client_hash, ec.ECDSA(hashes.SHA256()))
    att = {"fmt": "packed", "attStmt": {"alg": -7, "sig": signature}, "authData": auth_data}

    finish = s.post(base + "/register/finish", json={
        "clientDataJSON": b64u(client_data),
        "attestationObject": b64u(cbor(att)),
    })
    print("register/finish:", finish.status_code, finish.text.strip())

    abegin = s.get(base + "/assert/begin").json()
    achallenge = base64.urlsafe_b64decode(abegin["challenge"] + "==")
    aclient = json.dumps({
        "type": "webauthn.get",
        "challenge": b64u(achallenge),
        "origin": origin,
    }, separators=(",", ":")).encode()
    aclient_hash = hashlib.sha256(aclient).digest()
    aflags = 0x01 | 0x04
    rp_hash = hashlib.sha256(rp_id.encode()).digest()
    auth_assert = rp_hash + bytes([aflags]) + b"\x00\x00\x00\x00"
    asig = key.sign(auth_assert + aclient_hash, ec.ECDSA(hashes.SHA256()))

    afinish = s.post(base + "/assert/finish", json={
        "credentialId": b64u(cred_id),
        "clientDataJSON": b64u(aclient),
        "authenticatorData": b64u(auth_assert),
        "signature": b64u(asig),
    })
    print("assert/finish:", afinish.status_code, afinish.text.strip())


if __name__ == "__main__":
    main()
