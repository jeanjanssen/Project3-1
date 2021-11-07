import math as math

length_of_module1 = 0
length_of_module2 = 0
ny = 100
nx = 100


def getcoords(self, x, y):
    theta1 = math.atan2(ny, nx)
    theta3 = (x ^ 2 + y ^ 2 - length_of_module1 ^ 2 - length_of_module2 ^ 2) / (
                2 * length_of_module1 * length_of_module2)
    alpha = math.acos((x ^ 2 + y ^ 2 + length_of_module1 ^ 2 - length_of_module2 ^ 2) / (
                (2 * length_of_module1) * math.sqrt(x ^ 2 + y ^ 2)))
    beta = math.atan2(y, x)
    if theta3 < 0:
        theta2 = beta + alpha
    else:
        theta2 = beta - alpha
    theta4 = math.atan2(cos(theta)) - theta2 - theta3
