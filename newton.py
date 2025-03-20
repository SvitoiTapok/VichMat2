import math


def fx(x, y):
    return y/(math.cos(x*y+0.1)**2)-2*x
def fy(x,y):
    return x/(math.cos(x*y+0.1)**2)
def gx(x,y):
    return 2*x
def gy(x,y):
    return 4*y
def f(x,y):
    return x**2-math.tan(x*y+0.1)
def g(x,y):
    return 1-x**2-2*y**2

x = -0.1
y=0.7
print(fx(x, y), "dx +", fy(x,y), "dy =", f(x, y))
print(gx(x, y), "dx +", gy(x,y), "dy =", g(x, y))