import math as math
from numpy import *

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 12.5
output_list = []

def getcoords(px, py):
    # px and py are the desired points of the end-effector

    theta_1 = arctan2(px, py)
    theta_1 = rad2deg(theta_1)
    theta_1 = min(max(-45, theta_1), 45)

    phi = 90
    phi = deg2rad(phi)

    wx = px - l4 * cos(phi)
    wy = py - l4 * sin(phi)

    delta = wx ** 2 + wy ** 2
    c2 = (delta - l2 ** 2 - l3 ** 2) / (2 * l2 * l3)
    s2 = sqrt(1 - c2 ** 2)
    theta_3 = arctan2(s2, c2)

    s1 = ((l2 + l3 * c2) * wy - l3 * s2 * wx) / delta
    c1 = ((l2 + l3 * c2) * wx + l3 * s2 * wy) / delta
    theta_2 = arctan2(s1, c1)
    theta_4 = phi - theta_2 - theta_3

    theta_2 = rad2deg(theta_2)
    theta_2 = min(max(-45, theta_2), 45)
    theta_3 = rad2deg(theta_3)
    theta_3 = min(max(-45, theta_3), 45)
    theta_4 = rad2deg(theta_4)
    theta_4 = min(max(-90, theta_4), 90)

    # For every theta, getting the moves in a list with at most 5 degrees at a time,
    # so that the first motor moves at most 5 degrees until it is at its desired position,
    # then the second motor does the same, etc...
    t1 = 0
    for x in range(0, abs(math.floor(theta_1/5))):
        if theta_1 > 0:
            output_list.append('S, 0, 5, 0, 1, 0, 0, 2, 0, 0, 3, 0, 0')
            t1 += 1
        elif theta_1 < 0:
            output_list.append('S, 0, -5, 0, 1, 0, 0, 2, 0, 0, 3, 0, 0')
            t1 += 1
    if theta_1-5*t1 != 0:
        if theta_1 > 0:
            output_list.append('S, 0, {}, 0, 1, 0, 0, 2, 0, 0, 3, 0, 0'.format(theta_1 - 5 * t1))
        elif theta_1 < 0:
            output_list.append('S, 0, {}, 0, 1, 0, 0, 2, 0, 0, 3, 0, 0'.format(theta_1 + 5 * t1))

    t2 = 0
    for x in range(0, abs(math.floor(theta_2/5))):
        if theta_2 > 0:
            output_list.append('S, 0, 0, 0, 1, 5, 0, 2, 0, 0, 3, 0, 0')
            t2 += 1
        elif theta_2 < 0:
            output_list.append('S, 0, 0, 0, 1, -5, 0, 2, 0, 0, 3, 0, 0')
            t2 += 1
    if theta_2-5*t2 != 0:
        if theta_2 > 0:
            output_list.append('S, 0, 0, 0, 1, {}, 0, 2, 0, 0, 3, 0, 0'.format(theta_2-5*t2))
        elif theta_2 < 0:
            output_list.append('S, 0, 0, 0, 1, {}, 0, 2, 0, 0, 3, 0, 0'.format(theta_2 + 5 * t2))

    t3 = 0
    for x in range(0, abs(math.floor(theta_3/5))):
        if theta_3 > 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 5, 0, 3, 0, 0')
            t3 += 1
        elif theta_3 < 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, -5, 0, 3, 0, 0')
            t3 += 1
    if theta_3-5*t3 != 0:
        if theta_3 > 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, {}, 0, 3, 0, 0'.format(theta_3-5*t3))
        elif theta_3 < 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, {}, 0, 3, 0, 0'.format(theta_3 + 5 * t3))

    t4 = 0
    for x in range(0, abs(math.floor(theta_4 / 5))):
        if theta_4 > 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, 5, 0')
            t4 += 1
        elif theta_4 < 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, -5, 0')
            t4 += 1
    if theta_4 - 5 * t4 != 0:
        if theta_4 > 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, {}, 0'.format(theta_4 - 5 * t4))
        elif theta_4 < 0:
            output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, {}, 0'.format(theta_4 + 5 * t4))

    output = 'S, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0'.format(theta_1, theta_2, theta_3, theta_4)

    return print(*output_list, sep="\n")
    #return print(output)


getcoords(10, 15)
