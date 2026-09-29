import os

FLAG = os.getenv('FLAG').encode()
KEY = os.urandom(len(FLAG))


def xor(first, second):
    length = max(len(second), len(first))
    data = b''
    i, j = 0, 0
    for _ in range(length):
        data += (first[i] ^ second[j]).to_bytes(1, 'big')
        i += 1
        j += 1
        i %= len(first)
        j %= len(second)
        if i == 0 or j == 0:
            return data
    return data


if __name__ == "__main__":
    secret = xor(FLAG, KEY)
    print("Just encrypted my flag. Encrypt your data too, and let's join them together!")
    data = input("Your data > ").encode()
    print(secret + xor(data, KEY), sep="\n")