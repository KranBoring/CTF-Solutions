import ast
import hashlib
import os
import random
import secrets
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY_SIZE = 32
SALT_SIZE = 256

class SecureDotProductService:
    def __init__(self, key):
        self.key_vector = [byte for byte in key]
        self.salt = secrets.token_bytes(SALT_SIZE)
        self.trusted_vectors = self.generate_trusted_vectors()
        
    def hash_vector(self, vector):
        vector_encoding = vector[1:-1].encode('latin-1')
        return hashlib.sha512(self.salt + vector_encoding).digest().hex()

    def generate_trusted_vectors(self):
        trusted_vectors = []

        for _ in range(5):
            length = random.randint(1, 32)
            vector = [random.randint(-2**8, 2**8) for _ in range(length)]
            trusted_vectors.append((vector, self.hash_vector(str(vector))))

        return trusted_vectors
    
    def parse_vector(self, vector):
        sanitized = "".join(c if c in '0123456789,[]' else '' for c in vector)
        try:
            parsed = ast.literal_eval(sanitized)
        except (ValueError, SyntaxError, TypeError):
            return None
        
        if isinstance(parsed, list):
            return parsed
        return None
        
    def dot_product(self, vector):
        return sum(vector_entry * key_entry for vector_entry, key_entry in zip(vector, self.key_vector))
    
    def run(self):
        print("============== Secure Dot Product Service ==============")
        print("I will compute the dot product of my key vector with any trustworthy vector you choose!")
        print("Here are the vectors I trust won't leak my key:")

        for pair in self.trusted_vectors:
            print(pair)

        while True:
            print("========================================================")
            vector_input = input("Enter your vector: ")
            vector_input = vector_input.encode().decode('unicode_escape')
            vector = self.parse_vector(vector_input)
            vector_hash = self.hash_vector(vector_input)

            if not vector:
                print("Invalid vector! Please enter your vector as a list of ints.")
                continue

            input_hash = input("Enter its salted hash: ")
            
            if not vector_hash == input_hash:
                print("Untrusted vector detected!")
                break

            dot_product = self.dot_product(vector)

            print("The computed dot product is: " + str(dot_product))

def read_flag():
    flag_path = 'flag.txt'

    if os.path.exists(flag_path):
        with open(flag_path, 'r') as f:
            flag = f.read().strip()
    else:
        print("flag.txt not found in the current directory.")
        sys.exit()

    return flag

def encrypt_flag(flag, key):
    iv = secrets.token_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(flag.encode(), AES.block_size))

    return iv, ciphertext

def main():
    flag = read_flag()
    key = secrets.token_bytes(KEY_SIZE)
    iv, ciphertext = encrypt_flag(flag, key)

    print("==================== Encrypted Flag ====================")
    print(f"IV: {iv.hex()}")
    print(f"Ciphertext: {ciphertext.hex()}")

    service = SecureDotProductService(key)
    service.run()

if __name__ == "__main__":
    main()
