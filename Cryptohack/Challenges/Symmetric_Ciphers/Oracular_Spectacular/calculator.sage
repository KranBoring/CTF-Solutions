from sage.all import *
x, y = var('x y')
inner_sum(x) = sum(binomial(23, y) * (0.6)^y * (0.4)^(23 - y), y, x + 1, 23)
outer_sum = sum(binomial(23, x) * (0.4)^x * (0.6)^(23 - x) * (inner_sum(x))^15, x, 0, 23)
print(float(outer_sum))