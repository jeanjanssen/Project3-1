import math as math
from numpy import *

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 12.5


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

    output = 'S, 0, {}, 0, 1, {}, 0, 2, {}, 0, 3, {}, 0'.format(theta_1, theta_2, theta_3, theta_4)

    return print(output)
