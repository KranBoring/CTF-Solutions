import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.PublicKey import ECC

# ==========================================
# 1. HẰNG SỐ ĐƯỜNG CONG secp256k1
# ==========================================
# Group order n của secp256k1
ORDER_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


# ==========================================
# 2. BỘ PHÂN TÍCH ASN.1 DER THUẦN PYTHON
# ==========================================
def parse_tlv(data: bytes, pos: int = 0) -> tuple[int, bytes, int]:
  """Đọc một phần tử ASN.1 TLV (Tag-Length-Value)."""
  tag = data[pos]
  pos += 1
  length = data[pos]
  pos += 1
  if length & 0x80:
    n_bytes = length & 0x7F
    length = int.from_bytes(data[pos : pos + n_bytes], "big")
    pos += n_bytes
  val = data[pos : pos + length]
  return tag, val, pos + length


def parse_sequence_contents(val: bytes) -> list[tuple[int, bytes]]:
  """Tách các phần tử con bên trong một khối SEQUENCE."""
  items = []
  pos = 0
  while pos < len(val):
    tag, v, pos = parse_tlv(val, pos)
    items.append((tag, v))
  return items


def load_signet_der(filepath: str):
  """Bóc tách cấu trúc SignetBundle theo đúng schema trong case-note.txt."""
  raw = open(filepath, "rb").read()
  _, bundle_val, _ = parse_tlv(raw)
  bundle_items = parse_sequence_contents(bundle_val)

  # bundle_items[0]: version (INTEGER = 1)
  # bundle_items[1]: signer SPKI
  # bundle_items[2]: orders (SEQUENCE OF SignedOrder)
  # bundle_items[3]: seal (SealedOrder)

  orders_items = parse_sequence_contents(bundle_items[2][1])
  records = []

  for o_tag, o_val in orders_items:
    order_fields = parse_sequence_contents(o_val)
    seq = int.from_bytes(order_fields[0][1], "big")
    message = order_fields[1][1]

    # signature SEQUENCE { r INTEGER, s INTEGER }
    sig_fields = parse_sequence_contents(order_fields[2][1])
    r = int.from_bytes(sig_fields[0][1], "big")
    s = int.from_bytes(sig_fields[1][1], "big")

    # z_i = int_be(SHA-256(message_i)) mod n
    z = int.from_bytes(hashlib.sha256(message).digest(), "big") % ORDER_N
    records.append((seq, r, s, z))

  # seal: SEQUENCE { salt, nonce, ciphertext, tag }
  seal_fields = parse_sequence_contents(bundle_items[3][1])
  seal = {
      "salt": seal_fields[0][1],
      "nonce": seal_fields[1][1],
      "ciphertext": seal_fields[2][1],
      "tag": seal_fields[3][1],
  }

  return records, seal


# ==========================================
# 3. GIẢI HỆ PHƯƠNG TRÌNH MODULO N (CRAMER'S RULE)
# ==========================================
def det3(m: list[list[int]], n: int) -> int:
  """Tính định thức ma trận 3x3 modulo n."""
  return (
      m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
      - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
      + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
  ) % n


def recover_private_key(records: list[tuple[int, int, int, int]]) -> int:
  """Giải hệ phương trình 3 ẩn: s_i * k0 + (i * s_i) * delta - r_i * d = z_i (mod n)"""
  n = ORDER_N

  # Sử dụng 3 bản ghi đầu tiên: i = 0, 1, 2
  _, r0, s0, z0 = records[0]
  _, r1, s1, z1 = records[1]
  _, r2, s2, z2 = records[2]

  # Ma trận hệ số A cho vector ẩn [k0, delta, d]^T
  M = [
      [s0, 0, (n - r0) % n],
      [s1, s1, (n - r1) % n],
      [s2, (2 * s2) % n, (n - r2) % n],
  ]
  b = [z0, z1, z2]

  D = det3(M, n)
  D_inv = pow(D, -1, n)

  # Ma trận thay thế cột 2 (cột của d) bằng vector b
  M_d = [
      [M[0][0], M[0][1], b[0]],
      [M[1][0], M[1][1], b[1]],
      [M[2][0], M[2][1], b[2]],
  ]
  d = (det3(M_d, n) * D_inv) % n

  # Tính thêm k0 và delta để kiểm chứng với toàn bộ 6 bản ghi
  M_k0 = [
      [b[0], M[0][1], M[0][2]],
      [b[1], M[1][1], M[1][2]],
      [b[2], M[2][1], M[2][2]],
  ]
  k0 = (det3(M_k0, n) * D_inv) % n

  M_delta = [
      [M[0][0], b[0], M[0][2]],
      [M[1][0], b[1], M[1][2]],
      [M[2][0], b[2], M[2][2]],
  ]
  delta = (det3(M_delta, n) * D_inv) % n

  # Kiểm tra tính khớp nối với tất cả các chữ ký còn lại (i = 0..5)
  for i, r_i, s_i, z_i in records:
    k_i = (k0 + i * delta) % n
    assert (
        k_i * s_i - r_i * d - z_i
    ) % n == 0, f"[-] Xác thực thất bại tại record {i}!"

  print("[+] Khôi phục thành công khóa riêng ECDSA!")
  print(f"[+] k0    = 0x{k0:064x}")
  print(f"[+] delta = 0x{delta:064x}")
  print(f"[+] d     = 0x{d:064x}")
  return d


# ==========================================
# 4. HKDF-SHA-256 & GIẢI MÃ AES-GCM
# ==========================================
def hkdf_expand_sha256(
    ikm: bytes, salt: bytes, info: bytes, length: int = 32
) -> bytes:
  """Triển khai HKDF-SHA-256 chuẩn RFC 5869."""
  prk = hmac.new(salt, ikm, hashlib.sha256).digest()
  t = b""
  okm = b""
  i = 1
  while len(okm) < length:
    t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
    okm += t
    i += 1
  return okm[:length]


def decrypt_standing_order(d: int, seal: dict):
  # IKM = I2OSP(d, 32), unsigned big-endian
  ikm = d.to_bytes(32, "big")
  info = b"CSCTF26/TheSignet/v1/standing-order"

  aes_key = hkdf_expand_sha256(ikm, salt=seal["salt"], info=info, length=32)

  # Giải mã AES-256-GCM với nonce 12 bytes, tag 16 bytes, empty AAD
  cipher = AES.new(aes_key, AES.MODE_GCM, nonce=seal["nonce"])
  plaintext = cipher.decrypt_and_verify(seal["ciphertext"], seal["tag"])
  return plaintext.decode("utf-8")


if __name__ == "__main__":
  records, seal = load_signet_der("sealed-orders.der")
  print(f"[*] Đã bóc tách thành công {len(records)} đơn ký ECDSA.")

  private_key = recover_private_key(records)
  flag = decrypt_standing_order(private_key, seal)

  print("\n" + "=" * 50)
  print(f"FLAG: {flag}")
  print("=" * 50)