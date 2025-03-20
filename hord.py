def f(x):
    return -1.38 * x ** 3 - 5.42 * x ** 2 + 2.57 * x + 10.95
a = -1.4733
b = -1.451979083535503
prex = -1.451979083535503
x = (a*f(b)-b*f(a))/(f(b)-f(a))
print("a:", a)
print("b:", b)
print("x:", x)
print("f(a):", f(a))
print("f(b):", f(b))
print("f(x):", f(x))
print("x-x:", abs(x-prex))