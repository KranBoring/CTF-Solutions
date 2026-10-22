from sage.all import *

p = 28151
prime_factor = prime_factors(p - 1)
powers = [(p -1)/q for q in prime_factor]
for i in range(1 ,28151):
    if all([pow(i,int(power),p) != 1 for power in powers]):
        print(i)
        break
