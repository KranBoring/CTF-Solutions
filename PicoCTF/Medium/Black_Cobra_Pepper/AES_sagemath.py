from sage.all import *
from Crypto.Cipher import AES as PyCryptoAES
from Crypto.Util.Padding import pad


class AES:
    M_AFF = Matrix(GF(2), [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ])
    C_AFF = vector(GF(2), [1, 1, 0, 0, 0, 1, 1, 0])  # Hằng số 0x63

    def __init__(self, key: bytes):
        self.key = key
        self.x = PolynomialRing(GF(2), name="x").gen()
        self.F = GF(2**8, name="a", modulus=self.x**8 + self.x**4 + self.x**3 + self.x + 1)
        self.a = self.F.gen()
        # Ma trận khuếch tán MixColumns trên GF(2^8)
        a = self.a
        self.M_MIX = Matrix(self.F, [
            [a,     a + 1, 1,     1    ],
            [1,     a,     a + 1, 1    ],
            [1,     1,     a,     a + 1],
            [a + 1, 1,     1,     a    ],
        ])
        self.expand_key()

    @classmethod
    def new(cls, key: bytes):
        return cls(key)

    def _sbox(self, elem):
        inv = self.F(0) if elem == 0 else elem**(-1)
        bits = vector(GF(2), list(inv))
        return self.F(list(self.M_AFF * bits + self.C_AFF))

    def bytes2matrix(self, block: bytes):
        elems = [self.F.from_integer(b) for b in block]
        return Matrix(self.F, 4, 4, [elems[i : i + 4] for i in range(0, 16, 4)]).transpose()

    def matrix2bytes(self, mat) -> bytes:
        # Đọc theo từng cột (Column-Major) và chuyển đa thức GF(2^8) về số nguyên 0..255
        out = []
        for col in range(4):
            for row in range(4):
                elem = mat[row, col]
                val = elem.to_integer()
                out.append(val)
        return bytes(out)

    def expand_key(self):
        key_elems = [self.F.from_integer(b) for b in self.key]
        W = [vector(self.F, key_elems[4 * i : 4 * (i + 1)]) for i in range(4)]

        for i in range(4, 44):
            temp = W[i - 1]
            if i % 4 == 0:
                rot = vector(self.F, [temp[1], temp[2], temp[3], temp[0]])
                sub = vector(self.F, [self._sbox(el) for el in rot])
                rcon = vector(self.F, [self.a**(i // 4 - 1), self.F(0), self.F(0), self.F(0)])
                temp = sub + rcon
            W.append(W[i - 4] + temp)

        self.round_keys = [
            Matrix(self.F, W[4 * r : 4 * (r + 1)]).transpose() for r in range(11)
        ]

    def add_round_key(self, round_idx: int):
        self.state = self.state + self.round_keys[round_idx]

    def sub_bytes(self):
        self.state = self.state.apply_map(self._sbox)

    def shift_rows(self):
        # Xoay trái hàng r đi r ô
        self.state = Matrix(self.F, [
            list(self.state[r])[r:] + list(self.state[r])[:r] for r in range(4)
        ])

    def mix_columns(self):
        self.state = self.M_MIX * self.state

    def _encrypt_block(self, block: bytes) -> bytes:
        self.state = self.bytes2matrix(block)
        self.add_round_key(0)

        for r in range(1, 10):
            self.sub_bytes()
            self.shift_rows()
            self.mix_columns()
            self.add_round_key(r)

        # Vòng 10 bỏ qua MixColumns
        self.sub_bytes()
        self.shift_rows()
        self.add_round_key(10)

        return self.matrix2bytes(self.state)

    def encrypt_ecb(self, plaintext: bytes) -> bytes:
        padded = pad(plaintext, 16)
        return b"".join(
            self._encrypt_block(padded[i : i + 16]) for i in range(0, len(padded), 16)
        )


if __name__ == "__main__":
    key = b"0123456789abcdef"
    pt = b"Test AES-128 ECB mode implemented purely in SageMath!"

    my_ct = AES.new(key).encrypt_ecb(pt)
    ref_ct = PyCryptoAES.new(key, PyCryptoAES.MODE_ECB).encrypt(pad(pt, 16))

    assert my_ct == ref_ct
    print("[+] Khớp 100% với PyCryptodome:", my_ct.hex())