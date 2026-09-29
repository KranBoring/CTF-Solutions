with open("output.txt","r") as f:
    data = f.read().split(' ')
N = int(data[0], 10)
C_key = int(data[1])
iv = bytes.fromhex(data[2])
ct = bytes.fromhex(data[3])
E = 65537
print(N)
print(C_key)
print(iv)
print(ct)