import hashlib
import secrets

salt = secrets.token_bytes(256)

def hash_vector(vector):
    vector_encoding = vector[1:-1].encode('latin-1')
    print(vector_encoding)
    return hashlib.sha512(salt + vector_encoding).digest().hex()

vector = [1, 2, 3]
print(hash_vector(str(vector)))

print(str(vector).encode().decode().encode().decode('unicode_escape'))