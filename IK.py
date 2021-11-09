import math as math

a1 = 20.1
a2 = 13.4
a3 = 12.1
a4 = 12.5
z = 21.1


def getcoords(x, y):
    theta1 = math.atan(y / x)
    theta1 = min(max(theta1, -45), 45)
    # We think we need to limit the angle immediately to the ranges of the edmo modules, such that the calculations will
    # not go out of bounds.

    cq = math.sqrt((x - a1) ** 2 + y ** 2 + (z - theta1) ** 2)
    cp = math.sqrt((x - a1) ** 2 + y ** 2 + theta1 ** 2)

    alfa = math.acos((cq ** 2 + a2 ** 2 - a3 ** 2) / ((2 * cq) * a2))
    beta = math.acos((cq ** 2 + cp ** 2 - a4 ** 2) / ((2 * cq) * cp))
    gamma = (z - theta1) / math.sqrt((x - a1 ** 2) + y ** 2)

    theta2 = alfa + beta + gamma
    theta2 = min(max(theta2, -45), 45)
    theta3 = math.pi - math.acos((a2 ** 2 + a3 ** 2 - cq ** 2) / (2 * a2 * a3))
    theta3 = min(max(theta3, -45), 45)

    sigma = theta1 + theta2 + theta3

    theta4 = sigma - theta2 - theta3
    theta4 = min(max(theta4, -90), 90)

    output = 'S, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0'.format(theta1, theta2, theta3, theta4)

    return print(output)


getcoords(25.0, 25.0)
