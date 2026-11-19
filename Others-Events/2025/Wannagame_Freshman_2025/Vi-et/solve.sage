from sage.all import *

f(a,b,c) = a * b * c == 15864378984956659850534060107405422568891641699308509134070157505662198692417476378386001170963905568690006431674713
q(a,b,c) = a + b + c == 779122598205443694565344617967399722167
p(a,b,c) = a*b + b*c + c*a == 196487786916397904192643381759626074607590751745631772329891131596526673844879

P = solve([f,q,p],a,b,c)
for p in P:
    flag = f'W1{{{123*p[0].right()  + 456*p[1].right() + 789*p[2].right()}}}'
    print(flag)
from itertools import permutations
from sage.all import PolynomialRing, ZZ

s1 = 779122598205443694565344617967399722167  # a + b + c
s2 = (
    196487786916397904192643381759626074607590751745631772329891131596526673844879  # ab + bc + ca
)
s3 = (
    15864378984956659850534060107405422568891641699308509134070157505662198692417476378386001170963905568690006431674713  # abc
)

R = PolynomialRing(ZZ, "x")
x = R.gen()

P = x**3 - s1 * x**2 + s2 * x - s3
roots = [int(r) for r in P.roots(multiplicities=False)]
print(roots)
# Vì vai trò a, b, c đối xứng nên duyệt 6 hoán vị để lấy đúng thứ tự ban đầu
for a, b, c in permutations(roots):
	print(f"W1{{{123 * a + 456 * b + 789 * c}}}")