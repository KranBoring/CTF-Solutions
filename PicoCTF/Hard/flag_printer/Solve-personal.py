# %%
from sage.all import *

MOD = 7514777789
F = GF(MOD)
R = PolynomialRing(F, "x")
x = R.gen()

points = []
with open("encoded.txt", "r") as f:
	for line in f:
		if line.strip():
			xi, yi = map(int, line.split())
			points.append((F(xi), F(yi)))


# 1. Dựng cây tích con: M(x) = prod(x - x_i)
def build_tree(xs):
	if len(xs) == 1:
		return [x - xs[0]]
	mid = len(xs) // 2
	left = build_tree(xs[:mid])
	right = build_tree(xs[mid:])
	return [left[0] * right[0], left, right]


# 2. Tính giá trị M'(x) tại toàn bộ x_i từ trên xuống
def eval_tree(poly, tree, xs):
	if len(xs) == 1:
		return [poly[0]]
	mid = len(xs) // 2
	_, left, right = tree
	return eval_tree(poly % left[0], left, xs[:mid]) + eval_tree(
		poly % right[0], right, xs[mid:]
	)


# 3. Nội suy tuyến tính từ dưới lên: sum(w_i * M(x) / (x - x_i))
def interp_tree(weights, tree):
	if len(weights) == 1:
		return R(weights[0])
	mid = len(weights) // 2
	_, left, right = tree
	p_left = interp_tree(weights[:mid], left)
	p_right = interp_tree(weights[mid:], right)
	return p_left * right[0] + p_right * left[0]


xs = [p[0] for p in points]
ys = [p[1] for p in points]

tree = build_tree(xs)
M_prime = tree[0].derivative()
m_vals = eval_tree(M_prime, tree, xs)
weights = [y / m for y, m in zip(ys, m_vals)]
poly = interp_tree(weights, tree)

coeffs = [int(c) for c in poly.list()[:-1]]
with open("output.bmp", "wb") as f:
	f.write(bytearray(coeffs))
# %%
