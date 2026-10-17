import sympy as sp
import random 
from Crypto.Util.number import * 
a = getPrime(128)
b = getPrime(128)
c = getPrime(128)
x,y,z = sp.symbols('x y z')

print(f'a * b * c = {a*b*c}')
print(f'a + b + c = {a+b+c}')
print(f'a*b + b*c + c*a = {a*b + b*c + c*a}')

flag = f'W1{{{123*a  + 456*b + 789*c}}}'
"""
a * b * c = 15864378984956659850534060107405422568891641699308509134070157505662198692417476378386001170963905568690006431674713
a + b + c = 779122598205443694565344617967399722167
a*b + b*c + c*a = 196487786916397904192643381759626074607590751745631772329891131596526673844879
"""
