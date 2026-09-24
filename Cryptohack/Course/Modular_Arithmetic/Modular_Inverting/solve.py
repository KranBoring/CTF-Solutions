def xgcd(a , b):
    u,v,h,k = 1,0,0,1
    while a != 0:
        q, r = b // a, b % a
        x = h - u * q
        y = k - v * q
        a,b,u,v,h,k = r,a,x,y,u,v
    return b, h, k
gcd, x, y = xgcd(3,13)
print(y)