a = [588,665,216,113,642,4,836,114,851,492,819,237]
for p in range(100,1000):
    try:
        x = [(a[i+1] * pow(a[i], -1, p)) % p for i in range(len(a) - 1)]
        if len(set(x)) == 1:
            print(f"crypto{{{p},{x[1]}}}")
    except Exception:
        continue