#!/bin/python3

def e1(x, y):
    return x + y

def e2(x, y):
    return (x + y) + 2 * (x & y)


def o1(x):
    if x % 2: # 5 cannot be divided by 2, always true
        x = 1 << x
        x = 2 * x + 9
        return x

def o2(x):
    if ((4 * x * x + 4) % 19) != 0:
        x = 1 << x
        x = 2 * x + 9
        return x

def o3(x):
    if ((4 * x * x + 4) % 19) != 0:
        if x % 2:
            x = 1 << x
            x = 2 * x + 9
            return x
        else:
            x *= 5
            return x
    else:
        x += 85
        return x

print("These are some examples about mba and opaque obfuscation:")
print("Mba test e1 with 3 and 4 is: ", e1(3, 4))
print("Mba test e2 with 3 and 4 is:", e2(3, 4))

print("Opaque test o1: ", o1(5))
print("Opaque test o1: ", o2(5))
print("Opaque test o1: ", o3(5))


