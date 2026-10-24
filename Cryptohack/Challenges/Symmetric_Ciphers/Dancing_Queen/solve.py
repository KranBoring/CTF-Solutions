from chacha20 import ChaCha20,bytes_to_words, word, words_to_bytes, xor

msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
iv2 = bytes.fromhex('a99f9a7d097daabd2aa2a235')
msg_enc = bytes.fromhex('f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f')
flag_enc = bytes.fromhex('b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732')

def inverse_rotate(x, n):
    return ((x >> n) & 0xffffffff) | ((x << (32 - n)) & 0xffffffff)

keystream = xor(msg, msg_enc)[:64]

class recorver_key:
    def __init__(self):
        self.state = []
    
    def inverse_quarter_round(self, x ,a ,b ,c ,d):
        x[b] = inverse_rotate(x[b], 7); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
        x[d] = inverse_rotate(x[d], 8); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
        x[b] = inverse_rotate(x[b], 12); x[b] ^= x[c]; x[c] = word(x[c] - x[d])
        x[d] = inverse_rotate(x[d], 16); x[d] ^= x[a]; x[a] = word(x[a] - x[b])
    
    def inverse_inner_block(self, state):
        self.inverse_quarter_round(state, 3, 4, 9 , 14)
        self.inverse_quarter_round(state, 2, 7, 8, 13)
        self.inverse_quarter_round(state, 1, 6, 11, 12)
        self.inverse_quarter_round(state, 0, 5, 10, 15)
        self.inverse_quarter_round(state, 3, 7, 11 , 15)
        self.inverse_quarter_round(state, 2, 6, 10 , 14)
        self.inverse_quarter_round(state, 1, 5, 9 , 13)
        self.inverse_quarter_round(state, 0, 4, 8 , 12)

    def setup_state(self, keystream):
        self.state = bytes_to_words(keystream)

    def ChaCha20Key(self, keystream):
        self.setup_state(keystream)
        for _ in range(10):
            self.inverse_inner_block(self.state)
        return words_to_bytes(self.state[4:12])
    
Matrix = recorver_key()
key = Matrix.ChaCha20Key(keystream)
cipher = ChaCha20()
flag = cipher.decrypt(flag_enc, key, iv2)
print(flag)