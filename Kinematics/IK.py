import math as math
from numpy import *
from re import finditer
from Kinematics import FK

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 14

# Previous thetas such that the arm is (almost) up straight at the start
prevTheta1 = 0.0  # PEN4, bottom motor
prevTheta2 = -25.0  # PEN3
prevTheta3 = -45.0  # PEN2
prevTheta4 = -20.0  # PEN1, top motor

MAX_LENGTH = 100  # Maximum length of commandString (100 is consistent with the arduino code!)


def getAngles():
    """
    Returns
        prevTheta1 (angle PEN4), prevTheta2 (angle PEN3), prevTheta3 (angle PEN2), prevTheta4 (angle PEN1)
    """
    return prevTheta1, prevTheta2, prevTheta3, prevTheta4


def getcoords(px, py, pz):
    # px and py are the desired points of the end-effector

    if py <= 17.5:
        case = 1
    elif 17.5 < py <= 25.25:
        case = 2
    elif 25.25 < py <= 33:
        case = 3
    elif 33 < py:
        case = 4

    theta_1 = math.atan2(px, py)

    py = math.sqrt((px**2) + (py**2))

    if case == 1 or case == 2:
        theta_3 = 95
    elif case == 3 or case == 4:
        theta_3 = 50

    theta_3 = deg2rad(theta_3)

    la = getLengthTheta2Theta4(theta_3, l2, l3)
    lb = l4
    lc = math.sqrt((py**2) + (pz**2))
    print("la =", la, "\nlb =", lb, "\nlc =", lc, "\npy =", py)

    theta_a = math.acos((lb**2+lc**2-la**2)/(2*lb*lc))
    theta_b = math.acos((la**2+lc**2-lb**2)/(2*la*lc))
    theta_c = math.acos((la ** 2 + lb ** 2 - lc ** 2) /( 2 * la * lb))
    print("theta_a", theta_a, ", theta_b", theta_b, ", theta_c", theta_c, "\nwhole triangle:", theta_c+theta_b+theta_a)

    theta_d = math.acos((la**2+l3**2-l2**2)/(2*la*l3))
    print("theta_d", theta_d)
    theta_d += theta_c
    print("theta_d", theta_d)
    theta_d = math.pi - theta_d
    print("theta_d", theta_d)
    theta_d = rad2deg(theta_d)
    print(theta_d)
    print(theta_3)
    theta_4 = theta_d
    theta_4 -= 26.0
    print("theta_4", theta_4)
    theta_4 = min(max(-90, theta_4), 90)

    theta_e = math.acos((l2**2+la**2-l3**2)/(2*l2*la))
    print(theta_e)
    theta_e += theta_b
    print("theta_e", theta_e)
    print(rad2deg(theta_e))
    theta_e += math.atan(pz/py)
    print(theta_e)
    theta_2 = rad2deg(theta_e)
    theta_2 = 90 - theta_2





    # theta_4 = -math.atan((px ** 2 + pz ** 2 - la ** 2 - lb ** 2) / (2 * la * lb))
    #theta_4 = 2 * math.atan(
    #    (math.sqrt((la + lb) ** 2 - (pz ** 2 + py ** 2))) / (math.sqrt((pz ** 2 + py ** 2) - (la - lb) ** 2)))
    #theta_2 = math.atan(py / pz) - math.atan((lb * math.sin(theta_4)) / (la + lb * math.cos(theta_4)))

    # A = px - l4 * math.cos(theta_1) * math.cos(phi)
    # B = py - l4 * math.sin(theta_1) * math.cos(phi)
    # C = pz - l1 - l4 * math.sin(phi)
    #
    # theta_3 = math.acos((A ** 2 + B ** 2 + C ** 2 - l2 ** 2 - l3 ** 2) / (2 * l2 * l3))
    # # Take into account boundaries
    # theta_3 = rad2deg(theta_3)
    # theta_3 = min(max(10, theta_3), 100)
    # theta_3 = deg2rad(theta_3)
    print(theta_3)
    theta_3 = rad2deg(theta_3)
    print(theta_3)
    #
    # a = l3 * math.sin(theta_3)
    # b = l2 * l3 * math.cos(theta_3)
    # r = sqrt(a ** 2 + b ** 2)
    #
    # theta_2 = math.atan2(C, -sqrt(r ** 2 - C ** 2)) - math.atan2(a, b)
    theta_1 = rad2deg(theta_1)
    # print("Theta_1 =", theta_1)
    theta_1 = min(max(-45, theta_1), 45)
    theta_2 = min(max(-20, theta_2), 70)
    # theta_3 is commented out since we now use a predetermined angle
    # theta_3 = min(max(10, theta_3), 100)



    # Take into account offset
    #theta_2 -= 25
    #theta_3 -= 50

    # output = 'A,0,{:.2f},1000,1,{:.2f},1000,2,{:.2f},1000,3,{:.2f},1000\n'.format(theta_4, theta_3, theta_2, theta_1)
    # print(output)
    print("Theta1 =", theta_1, "\nTheta2 =", theta_2, "\nTheta3 =", theta_3, "\nTheta4 =", theta_4)
    return theta_1, theta_2, theta_3, theta_4
    #return make_list(theta_1, theta_2, theta_3, theta_4)


def getLengthTheta2Theta4(theta3, l2, l3):  # l2 and l3 can be taken from the class FK
    """
    Method to get the length between theta2 and theta4
    Takes as input theta3, length2 and length3
    Returns the length between theta2 and theta4
    """
    length_t2_t4 = math.sqrt((l3**2) + (l2**2) - (2 * l3 * l2 * math.cos(math.pi-theta3)))
    return length_t2_t4


def make_list(theta_1, theta_2, theta_3, theta_4):
    # For every theta, getting the moves in a list with at most 5 degrees at a time,
    # so that the first motor moves at most 5 degrees until it is at its desired position,
    # then the second motor does the same, etc...
    output_list = []

    # First, make the commandString for PEN1 (theta_4), i.e., the top motor,
    # taking into account the previous angle
    global prevTheta4
    angleDiff = theta_4 - prevTheta4
    if angleDiff != 0:
        # Make the commandString
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
        output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta4 = theta_4  # Update prevTheta4

    # Make the commandString for PEN2 (theta_3), i.e., the second motor from the top,
    # taking into account the previous angle
    global prevTheta3
    angleDiff = theta_3 - prevTheta3
    if angleDiff != 0:
        # Make the commandString
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
        output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta3 = theta_3  # Update prevTheta3

    # Make the commandString for PEN4 (theta_1), i.e., the bottom motor,
    # taking into account the previous angle
    global prevTheta1
    angleDiff = theta_1 - prevTheta1
    if angleDiff != 0:
        # Make the commandString
        commandString = "A"
        t1 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",3,{:.0f},1000".format(prevTheta1 + 5 * (t1 + 1))
                t1 += 1
            elif angleDiff < 0:
                commandString += ",3,{:.0f},1000".format(prevTheta1 - 5 * t1)
                t1 += 1
        if angleDiff - 5 * t1 != 0:
            commandString += ",3,{:.2f},1000".format(theta_1)
        output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta1 = theta_1  # Update prevTheta1

    # Lastly, make the commandString for PEN3 (theta_2),
    # taking into account the previous angle
    global prevTheta2
    angleDiff = theta_2 - prevTheta2
    if angleDiff != 0:
        # Make the commandString
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
        output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta2 = theta_2  # Update prevTheta2

    return output_list


def constrainCommandStringLength(commandString):
    # If the commandString is longer than 100 characters, cut them up into commandStrings with a max length of 100
    commandStringList = []
    while len(commandString) > MAX_LENGTH:
        # Get the indices of where the commas are
        commaIndices = finditer(',', commandString[0:MAX_LENGTH])
        commaIndices = [commaIndex.start() for commaIndex in commaIndices]

        # Get cutoffPoint
        maxCommaIndex = len(commaIndices) - 1
        if maxCommaIndex % 3 == 0:
            cutoffPoint = commaIndices[maxCommaIndex]
        else:
            cutoffPoint = commaIndices[maxCommaIndex - (maxCommaIndex % 3)]

        # Split commandStrings
        commandStringList.append(commandString[0:cutoffPoint] + "\n")
        commandString = "A" + commandString[cutoffPoint:]

    # Append last commandString
    commandStringList.append(commandString)
    # print(commandStringList)
    return commandStringList


def move_kinematics(player):
    if player == 'X':
        pass
    elif player == 'O':
        pass


if __name__ == '__main__':
    output = getcoords(-10, 20, 1)
    print(FK.calc_position(output[0], output[1], output[2], output[3]))
    #for x in output:
    #    print("sending", x, end="")


