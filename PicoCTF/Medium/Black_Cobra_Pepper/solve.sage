from sage.all import GF, Matrix, vector
import os

# ==========================================
# 1. Triển khai AES không có SubBytes / SubWord
# ==========================================

# Bảng nhân x (nhân 0x02 trong GF(2^8) với đa thức xtime chuẩn của AES)
def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

def mix_single_column(a):
    # Phép nhân ma trận MixColumns chuẩn: [2 3 1 1; 1 2 3 1; 1 1 2 3; 3 1 1 2]
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a0 = a[0] ^ t ^ xtime(a[0] ^ a[1])
    a1 = a[1] ^ t ^ xtime(a[1] ^ a[2])
    a2 = a[2] ^ t ^ xtime(a[2] ^ a[3])
    a3 = a[3] ^ t ^ xtime(a[3] ^ u)
    return [a0, a1, a2, a3]

def mix_columns(state):
    res = [0] * 16
    for c in range(4):
        col = [state[c + 4 * r] for r in range(4)]
        mixed = mix_single_column(col)
        for r in range(4):
            res[c + 4 * r] = mixed[r]
    return res

def shift_rows(state):
    # Hoán vị dịch hàng chuẩn
    res = [0] * 16
    # Row 0: shift 0
    res[0], res[4], res[8], res[12] = state[0], state[4], state[8], state[12]
    # Row 1: shift 1
    res[1], res[5], res[9], res[13] = state[5], state[9], state[13], state[1]
    # Row 2: shift 2
    res[2], res[6], res[10], res[14] = state[10], state[14], state[2], state[6]
    # Row 3: shift 3
    res[3], res[7], res[11], res[15] = state[15], state[3], state[7], state[11]
    return res

# Rcon cho 10 vòng
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def key_expansion_no_sbox(key_bytes):
    # Key expansion tuyến tính (loại bỏ SubWord, giữ RotWord và Rcon)
    w = [b for b in key_bytes]
    for i in range(4, 44):
        tmp = w[4 * (i - 1): 4 * i]
        if i % 4 == 0:
            # RotWord
            tmp = tmp[1:] + tmp[:1]
            # KHÔNG gọi SubWord
            tmp[0] ^= RCON[(i // 4) - 1]
        for j in range(4):
            w.append(w[4 * (i - 4) + j] ^ tmp[j])
    return [w[16 * r: 16 * (r + 1)] for r in range(11)]

def aes_encrypt_no_sbox(plaintext, key):
    round_keys = key_expansion_no_sbox(key)
    state = [p ^ k for p, k in zip(plaintext, round_keys[0])]
    
    for r in range(1, 10):
        # KHÔNG có sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = [s ^ k for s, k in zip(state, round_keys[r])]
        
    # Vòng cuối không có MixColumns
    state = shift_rows(state)
    state = [s ^ k for s, k in zip(state, round_keys[10])]
    return state

# ==========================================
# 2. Xử lý biểu diễn Vector trên GF(2)
# ==========================================

def bytes_to_gf2_vector(b_arr):
    bits = []
    for byte in b_arr:
        for bit_idx in range(8):
            bits.append((byte >> (7 - bit_idx)) & 1)
    return vector(GF(2), bits)

def gf2_vector_to_bytes(v):
    b_arr = []
    for byte_idx in range(16):
        byte_val = 0
        for bit_idx in range(8):
            byte_val = (byte_val << 1) | int(v[byte_idx * 8 + bit_idx])
        b_arr.append(byte_val)
    return bytes(b_arr)

# ==========================================
# 3. Dựng hệ phương trình & Khôi phục khóa
# ==========================================

print("[+] Khởi tạo kịch bản tấn công Known-Plaintext Attack...")
TARGET_KEY = os.urandom(16)
PLAINTEXT = b"Hello Linear AES"
CIPHERTEXT = bytes(aes_encrypt_no_sbox(list(PLAINTEXT), list(TARGET_KEY)))

print(f"[*] Plaintext : {PLAINTEXT.hex()}")
print(f"[*] Ciphertext: {CIPHERTEXT.hex()}")
print(f"[*] Secret Key: {TARGET_KEY.hex()} (Cần khôi phục)")

# Tính hằng số vòng dịch tự do C_0 khi P=0, K=0
zero_16 = [0] * 16
c0_vector = bytes_to_gf2_vector(aes_encrypt_no_sbox(zero_16, zero_16))

# Trích xuất 128 cột của ma trận M_K
print("[+] Đang dựng ma trận tuyến tính 128x128 trên GF(2)...")
columns = []
for bit_idx in range(128):
    # Vector cơ sở e_j
    k_test = [0] * 16
    k_test[bit_idx // 8] |= (1 << (7 - (bit_idx % 8)))
    
    # E(0, e_j) ^ C_0 = M_K * e_j (chính là cột thứ bit_idx của M_K)
    c_out = bytes_to_gf2_vector(aes_encrypt_no_sbox(zero_16, k_test))
    col = c_out + c0_vector
    columns.append(col)

M_K = Matrix(GF(2), columns).transpose()

# Thiết lập vế phải: Target = Ciphertext ^ AES(Plaintext, 0)
c_target_vector = bytes_to_gf2_vector(list(CIPHERTEXT))
p_only_vector = bytes_to_gf2_vector(aes_encrypt_no_sbox(list(PLAINTEXT), zero_16))
rhs_vector = c_target_vector + p_only_vector

# Giải hệ: M_K * K = rhs
print("[+] Đang giải hệ phương trình bằng phép khử Gauss...")
recovered_key_vector = M_K.solve_right(rhs_vector)
recovered_key = gf2_vector_to_bytes(recovered_key_vector)

print(f"[+] Khóa khôi phục được: {recovered_key.hex()}")
assert recovered_key == TARGET_KEY, "Khôi phục thất bại!"
print("[+] Thành công! Khóa khớp 100% với Secret Key ban đầu.")