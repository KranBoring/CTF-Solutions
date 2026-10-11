from pathlib import Path

path = Path("koblitz.py")
src = path.read_text()

old = '''def sq_root_mod_n(n, p):
    n = n % p
    for x in range(2, p):
        if ((x*x) % p == n):
            return x
    return 0
'''
new = '''def sq_root_mod_n(n, p):
    n %= p
    y = pow(n, (p + 1) // 4, p)
    return y if y * y % p == n else 0
'''

assert old in src
assert 'def koblitz_encoder(plainText, elliptic_a, elliptic_b):' in src
assert '    p = 751\n' in src

src = src.replace(old, new)
src = src.replace(
    'def koblitz_encoder(plainText, elliptic_a, elliptic_b):',
    'def koblitz_encoder(plainText, elliptic_a, elliptic_b, p):',
)
src = src.replace('    p = 751\n', '')

path.write_text(src)
