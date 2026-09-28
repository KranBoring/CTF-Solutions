def decode_flag(flag):
    result = []
    for char in flag:
        if isinstance(char, int):
            result.append(chr(char + ord('A') - 1))
        else:
            result.append(char)
    return ''.join(result)

flag = [16, 9, 3, 15, 3, 20, 6, "{", 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 3, 1, 19, 15, 14, "}"]
print(decode_flag(flag))