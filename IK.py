import math as math
from numpy import *

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 12.5
output_list = []

def getcoords(px, py):
    # px and py are the desired points of the end-effector

    phi = 90
    phi = deg2rad(phi)

    wx = px - l4 * cos(phi)
    wy = py - l4 * sin(phi)

    theta_1 = math.atan2(wx, wy)
    theta_1 = rad2deg(theta_1)
    theta_1 = min(max(-45, theta_1), 45)
    theta_1 = int(theta_1)

    delta = wx ** 2 + wy ** 2
    c2 = (delta - l2 ** 2 - l3 ** 2) / (2 * l2 * l3)
    s2 = sqrt(1 - c2 ** 2)
    theta_3 = arctan2(s2, c2)

    s1 = ((l2 + l3 * c2) * wy - l3 * s2 * wx) / delta
    c1 = ((l2 + l3 * c2) * wx + l3 * s2 * wy) / delta
    theta_2 = arctan2(s1, c1)
    theta_4 = phi - (theta_2 + theta_3)

    theta_2 = rad2deg(theta_2)
    theta_2 = min(max(-45, theta_2), 45)
    theta_2 = int(theta_2)
    theta_2 = theta_2*-1
    theta_3 = rad2deg(theta_3)
    theta_3 = min(max(-45, theta_3), 45)
    theta_3 = int(theta_3)
    theta_4 = rad2deg(theta_4) - (21.801 + 5.654)
    theta_4 = min(max(-90, theta_4), 90)
    theta_4 = int(theta_4)

    # For every theta, getting the moves in a list with at most 5 degrees at a time,
    # so that the first motor moves at most 5 degrees until it is at its desired position,
    # then the second motor does the same, etc...
    t1 = 0
    for x in range(0, abs(math.floor(theta_1/5))):
        if theta_1 > 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, {}, 0\n'.format(5*(t1+1)))
            t1 += 1
        elif theta_1 < 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, {}, 0\n'.format(-5*(t1+1)))
            t1 += 1
    if theta_1-5*t1 != 0:
        if theta_1 > 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, {}, 0\n'.format(theta_1 - 5 * t1))
        elif theta_1 < 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, {}, 0\n'.format(theta_1 + 5 * t1))

    t2 = 0
    for x in range(0, abs(math.floor(theta_2/5))):
        if theta_2 > 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, {}, 0, 3, {}, 0\n'.format(5*(t2+1), theta_1))
            t2 += 1
        elif theta_2 < 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, {}, 0, 3, {}, 0\n'.format(-5*(t2+1). theta_1))
            t2 += 1
    if theta_2-5*t2 != 0:
        if theta_2 > 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, {}, 0, 3, {}, 0\n'.format(theta_2-5*t2, theta_1))
        elif theta_2 < 0:
            output_list.append('0, 0, 0, 0, 1, 0, 0, 2, {}, 0, 3, {}, 0\n'.format(theta_2 + 5 * t2, theta_1))

    t3 = 0
    for x in range(0, abs(math.floor(theta_3/5))):
        if theta_3 > 0:
            output_list.append('0, 0, 0, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(5*(t3+1), theta_2, theta_1))
            t3 += 1
        elif theta_3 < 0:
            output_list.append('0, 0, 0, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(-5*(t3+1), theta_2, theta_1))
            t3 += 1
    if theta_3-5*t3 != 0:
        if theta_3 > 0:
            output_list.append('0, 0, 0, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(theta_3-5*t3, theta_2, theta_1))
        elif theta_3 < 0:
            output_list.append('0, 0, 0, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(theta_3 + 5 * t3, theta_2, theta_1))

    t4 = 0
    for x in range(0, abs(math.floor(theta_4 / 5))):
        if theta_4 > 0:
            output_list.append('0, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(5*(t4+1), theta_3, theta_2, theta_1))
            t4 += 1
        elif theta_4 < 0:
            output_list.append('0, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(-5*(t4+1), theta_3, theta_2, theta_1))
            t4 += 1
    if theta_4 - 5 * t4 != 0:
        if theta_4 > 0:
            output_list.append('0, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(theta_4 - 5 * t4), theta_3, theta_2, theta_1)
        elif theta_4 < 0:
            output_list.append('0, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0\n'.format(theta_4 + 5 * t4), theta_3, theta_2, theta_1)

    output = 'A,0,{},0,1,{},0,2,{},0,3,{},0\n'.format(theta_4, theta_3, theta_2, theta_1)

    #print(*output_list)
    print(output)
    return output
