flag = b'crypto{????????????????????}'
plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
print(plaintext)
a = 288260533169915
p = 1007621497415251
if pow(a, (p-1)//2,p) == 1:
    print(f"{a} la 1 so co thang du bac 2")
if (p % 4 == 3):
    print(f"{p} mod 4 = 3")