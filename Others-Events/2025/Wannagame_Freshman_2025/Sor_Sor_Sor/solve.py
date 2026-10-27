from pwn import xor
import string

ciphertext = bytes.fromhex("2f01090a6f042b4447101f0047460d6e0e5d001100422d156443022c4a3e074a392b033e531d1b47401b44423c411e08")
cipher_blocks = [ciphertext[i:i + 3] for i in range(0, len(ciphertext), 3)]
leng = len(cipher_blocks)

value_check = (string.ascii_letters + string.digits + "_").encode()

def right_flag(index, val):
    if index == 0:
        return val == b"W1{"
    if index == leng - 1:
        return val[2:] == b"}" and all(char in value_check for char in val[:2])
    return all(char in value_check for char in val)

def find_hamiliton(start_index, start_value):
    result = []
    def dfs(curr_index, curr_val, path):
        next_value = xor(curr_val, cipher_blocks[curr_index])
        if next_value == start_value:
            result.append(path)
            return
        for next_index in range(leng):
            if next_index not in path and next_index != curr_index:
                if right_flag(next_index, next_value):
                    dfs(next_index, next_value, path | {next_index: next_value})
    dfs(start_index, start_value, {start_index: start_value})
    return result

cy0 = find_hamiliton(0, b"W1{")

for c0 in cy0:
    print(b"".join([c0[i] for i in range(leng)]))
