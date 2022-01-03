import math as math
from numpy import *

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 12.5

prevTheta1 = 0
prevTheta2 = 0
prevTheta3 = 0
prevTheta4 = 0


def getcoords(px, py, pz, phi):
    # px and py are the desired points of the end-effector
    px = px / 30.5
    py = py / 42.5

    phi = deg2rad(phi)

    theta_1 = math.atan2(py, px)

    A = px - l4 * math.cos(theta_1) * math.cos(phi)
    B = py - l4 * math.sin(theta_1) * math.cos(phi)
    C = pz - l1 - l4 * math.sin(phi)

    theta_3 = math.acos((A ** 2 + B ** 2 + C ** 2 - l2 ** 2 - l3 ** 2) / (2 * l2 * l3))

    a = l3 * math.sin(theta_3)
    b = l2 * l3 * math.cos(theta_3)
    r = sqrt(a ** 2 + b ** 2)

    theta_2 = math.atan2(C, -sqrt(r ** 2 - C ** 2)) - math.atan2(a, b)
    # delta = wx ** 2 + wy ** 2
    # c2 = (delta - l2 ** 2 - l3 ** 2) / (2 * l2 * l3)
    # s2 = sqrt(1 - c2 ** 2)
    # theta_3 = arctan2(s2, c2)
    #
    # s1 = ((l2 + l3 * c2) * wy - l3 * s2 * wx) / delta
    # c1 = ((l2 + l3 * c2) * wx + l3 * s2 * wy) / delta
    # theta_2 = arctan2(s1, c1)

    phi = rad2deg(phi)
    theta_1 = rad2deg(theta_1)
    # print("Theta_1 =", theta_1)
    theta_1 = min(max(-45, theta_1), 45)
    theta_2 = rad2deg(theta_2)
    theta_2 = min(max(-45, theta_2), 45)
    theta_2 = theta_2 * -1
    theta_3 = rad2deg(theta_3)
    theta_3 = min(max(-45, theta_3), 45)
    theta_4 = phi - theta_2 - theta_3
    theta_4 = min(max(-90, theta_4), 90)

    # For every theta, getting the moves in a list with at most 5 degrees at a time,
    # so that the first motor moves at most 5 degrees until it is at its desired position,
    # then the second motor does the same, etc...
    output_list = []

    #"""
    # First, make the commandString for PEN1 (theta_4), i.e., the top motor,
    # taking into account the previous angle
    global prevTheta4
    angleDiff = theta_4 - prevTheta4
    if angleDiff != 0:
        commandString = "A"
        t4 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",0,{:.0f},1000".format(prevTheta4 + 5 * (t4 + 1))
                t4 += 1
            elif angleDiff < 0:
                commandString += ",0,{:.0f},1000".format(prevTheta4 - 5 * t4)
                t4 += 1
        if angleDiff - 5 * t4 != 0:
            commandString += ",0,{:.2f},1000".format(theta_4)
        commandString += "\n"
        output_list.append(commandString)
        prevTheta4 = theta_4    # Update prevTheta4


    # Make the commandString for PEN2 (theta_3), i.e., the second motor from the top,
    # taking into account the previous angle
    global prevTheta3
    angleDiff = theta_3 - prevTheta3
    if angleDiff != 0:
        commandString = "A"
        t3 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",1,{:.0f},1000".format(prevTheta3 + 5 * (t3 + 1))
                t3 += 1
            elif angleDiff < 0:
                commandString += ",1,{:.0f},1000".format(prevTheta3 - 5 * t3)
                t3 += 1
        if angleDiff - 5 * t3 != 0:
            commandString += ",1,{:.2f},1000".format(theta_3)
        commandString += "\n"
        output_list.append(commandString)
        prevTheta3 = theta_3    # Update prevTheta3

    # Make the commandString for PEN4 (theta_1), i.e., the bottom motor,
    # taking into account the previous angle
    commandString = "A"
    t1 = 0
    global prevTheta1
    angleDiff = theta_1 - prevTheta1
    for x in range(0, abs(math.floor(angleDiff / 5))):
        if angleDiff > 0:
            commandString += ",3,{:.0f},1000".format(prevTheta1 + 5 * (t1 + 1))
            t1 += 1
        elif angleDiff < 0:
            commandString += ",3,{:.0f},1000".format(prevTheta1 - 5 * t1)
            t1 += 1
    if angleDiff - 5 * t1 != 0:
        commandString += ",3,{:.2f},1000".format(theta_1)
    commandString += "\n"
    output_list.append(commandString)
    prevTheta1 = theta_1    # Update prevTheta1

    # Lastly, make the commandString for PEN3 (theta_2),
    # taking into account the previous angle
    global prevTheta2
    angleDiff = theta_2 - prevTheta2
    if angleDiff != 0:
        commandString = "A"
        t2 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 + 5 * (t2 + 1))
                t2 += 1
            elif angleDiff < 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 - 5 * t2)
                t2 += 1
        if angleDiff - 5 * t2 != 0:
            commandString += ",2,{:.2f},1000".format(theta_2)
        commandString += "\n"
        output_list.append(commandString)
        prevTheta2 = theta_2    # Update prevTheta2
    #"""

    """
    # First, make the commandString for PEN1 (theta_4), i.e., the top motor
    commandString = "A"
    t4 = 0
    for x in range(0, abs(math.floor(theta_4 / 5))):
        if theta_4 > 0:
            commandString += ",0,{},1000".format(5 * (t4 + 1))
            t4 += 1
        elif theta_4 < 0:
            commandString += ",0,{},1000".format(-5 * t4)
            t4 += 1
    if theta_4 - 5 * t4 != 0:
        commandString += ",0,{:.2f},1000".format(theta_4)
    commandString += "\n"
    output_list.append(commandString)

    # Make the commandString for PEN2 (theta_3), i.e., the second motor from the top
    commandString = "A"
    t3 = 0
    for x in range(0, abs(math.floor(theta_3 / 5))):
        if theta_3 > 0:
            commandString += ",1,{},1000".format(5 * (t3 + 1))
            t3 += 1
        elif theta_3 < 0:
            commandString += ",1,{},1000".format(-5 * t3)
            t3 += 1
    if theta_3 - 5 * t3 != 0:
        commandString += ",1,{:.2f},1000".format(theta_3)
    commandString += "\n"
    output_list.append(commandString)

    # Make the commandString for PEN4 (theta_1), i.e., the bottom motor
    commandString = "A"
    t1 = 0
    for x in range(0, abs(math.floor(theta_1 / 5))):
        if theta_1 > 0:
            commandString += ",3,{},1000".format(5 * (t1 + 1))
            t1 += 1
        elif theta_1 < 0:
            commandString += ",3,{},1000".format(-5 * (t1 + 1))
            t1 += 1
    if theta_1 - 5 * t1 != 0:
        commandString += ",3,{:.2f},1000".format(theta_1)
    commandString += "\n"
    output_list.append(commandString)

    # Lastly, make the commandString for PEN3 (theta_2)
    commandString = "A"
    t2 = 0
    for x in range(0, abs(math.floor(theta_2 / 5))):
        if theta_2 > 0:
            commandString += ",2,{},1000".format(5 * (t2 + 1))
            t2 += 1
        elif theta_2 < 0:
            commandString += ",2,{},1000".format(-5 * t2)
            t2 += 1
    if theta_2 - 5 * t2 != 0:
        commandString += ",2,{:.2f},1000".format(theta_2)
    commandString += "\n"
    output_list.append(commandString)
    """

    for commandString in output_list:
        print(commandString, end="")

    # output = 'A,0,{:.2f},1000,1,{:.2f},1000,2,{:.2f},1000,3,{:.2f},1000\n'.format(theta_4, theta_3, theta_2, theta_1)
    # print(output)

    return output_list
