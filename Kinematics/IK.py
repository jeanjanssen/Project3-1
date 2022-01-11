import math
from numpy import *
from re import finditer
from Kinematics import FK

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 14  # length to the pen

# Previous thetas such that the arm is (almost) up straight at the start
prevTheta1 = 0.0    # PEN4, bottom motor
prevTheta2 = -25.0  # PEN3
prevTheta3 = -45.0  # PEN2
prevTheta4 = -20.0  # PEN1, top motor

MAX_LENGTH = 100  # Maximum length of commandString (100 is consistent with arduino code! Don't enter higher values!)


def getAngles():
    """ Returns prevTheta1 (angle PEN4), prevTheta2 (angle PEN3), prevTheta3 (angle PEN2), prevTheta4 (angle PEN1) """
    return prevTheta1, prevTheta2, prevTheta3, prevTheta4


def getcoords(px, py, pz):
    # px and py are the desired points of the end-effector

    if py <= 17.5:
        case = 1
    elif 17.5 < py <= 25.25:
        case = 2
    elif 25.25 < py <= 33:
        case = 3
    elif 33 > py:
        case = 4

    theta_1 = math.atan2(px, py)

    py = math.sqrt((px ** 2) + (py ** 2))

    if case == 1 or case == 2:
        theta_3 = 95
    elif case == 3 or case == 4:
        theta_3 = 50

    theta_3 = deg2rad(theta_3)

    la = getLengthTheta2Theta4(theta_3, l2, l3)
    lb = l4
    lc = math.sqrt((py ** 2) + (pz ** 2))
    print("la =", la, "\nlb =", lb, "\nlc =", lc, "\npy =", py)

    # TODO remove theta_a and theta_b since we only need theta_c???
    theta_a = math.acos((lb ** 2 + lc ** 2 - la ** 2) / (2 * lb * lc))
    theta_b = math.acos((la ** 2 + lc ** 2 - lb ** 2) / (2 * la * lc))
    theta_c = math.acos((la ** 2 + lb ** 2 - lc ** 2) / (2 * la * lb))
    print("theta_a", theta_a, ", theta_b", theta_b, ", theta_c", theta_c, "\nwhole triangle:",
          theta_c + theta_b + theta_a)

    theta_d = math.acos((la ** 2 + l3 ** 2 - l2 ** 2) / (2 * la * l3))
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

    theta_e = math.acos((l2 ** 2 + la ** 2 - l3 ** 2) / (2 * l2 * la))
    print(theta_e)
    theta_e += theta_b
    print("theta_e", theta_e)
    print(rad2deg(theta_e))
    theta_e += math.atan(pz / py)
    print(theta_e)
    theta_2 = rad2deg(theta_e)
    theta_2 = 90 - theta_2

    # theta_4 = -math.atan((px ** 2 + pz ** 2 - la ** 2 - lb ** 2) / (2 * la * lb))
    # theta_4 = 2 * math.atan(
    #    (math.sqrt((la + lb) ** 2 - (pz ** 2 + py ** 2))) / (math.sqrt((pz ** 2 + py ** 2) - (la - lb) ** 2)))
    # theta_2 = math.atan(py / pz) - math.atan((lb * math.sin(theta_4)) / (la + lb * math.cos(theta_4)))

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

    # output = 'A,0,{:.2f},1000,1,{:.2f},1000,2,{:.2f},1000,3,{:.2f},1000\n'.format(theta_4, theta_3, theta_2, theta_1)
    # print(output)
    print("Theta1 =", theta_1, "\nTheta2 =", theta_2, "\nTheta3 =", theta_3, "\nTheta4 =", theta_4)
    return theta_1, theta_2, theta_3, theta_4


# second try
def getCoords2(px, py, pz):
    """
    returns angles in degrees
    """
    theta1 = math.atan(px / py)
    theta1 = rad2deg(theta1)

    a = math.sqrt(py ** 2 + px ** 2) - l4
    b = pz - l1

    # theta3 = - math.acos((a ** 2 + b ** 2 - l2 ** 2 - l3 ** 2) / (2 * l2 * l3))
    value = (a ** 2 + b ** 2 - l2 ** 2 - l3 ** 2) / (2 * l2 * l3)
    # print(value**2)
    theta3 = - math.atan(math.sqrt(1 - value ** 2) / value)

    theta2prime = math.atan(b / a) + math.atan((l3 * math.sin(theta3)) / (l2 + l3 * math.cos(theta3)))
    theta2prime = rad2deg(theta2prime)

    theta3 = rad2deg(theta3)

    theta2 = theta2prime - 90

    theta4 = 90 - theta2prime - theta3

    print("Theta1 =", theta1, "\nTheta2 =", theta2prime, "\nTheta3 =", theta3, "\nTheta4 =", theta4)
    # Take into account offset
    theta2 -= 25
    theta3 -= 50
    theta4 -= 20

    # TODO consider motors range

    return make_list(theta1, theta2, theta3, theta4)


def getLengthTheta2Theta4(theta3, l2, l3):  # l2 and l3 can be taken from the class FK
    """
    Method to get the length between theta2 and theta4
    Takes as input theta3, length2 and length3
    Returns the length between theta2 and theta4
    """
    length_t2_t4 = math.sqrt((l3 ** 2) + (l2 ** 2) - (2 * l3 * l2 * math.cos(math.pi - theta3)))
    return length_t2_t4


def make_list(theta_1, theta_2, theta_3, theta_4):
    """ Makes a list of commandStrings which are to be sent to the motors

    For every theta, getting the moves in a list with at most 5 degrees at a time,
    so that the first motor moves at most 5 degrees until it is at its desired position,
    then the second motor does the same, etc...

    Parameters
    ----------
        theta_1 : float
            Angle of the bottom motor (PEN4) in degrees
        theta_2 : float
            Angle of the third motor (PEN3) in degrees
        theta_3 : float
            Angle of the second motor (PEN2) in degrees
        theta_4 : float
            Angle of the top motor (PEN1) in degrees

    Returns a list of commandStrings to be sent to the motors
    """

    # TODO method now makes one big list, might still need some tweaking

    # Initialize output_list
    output_list = []
    commandString = "A"

    # First, make the commandString for PEN1 (theta_4), i.e., the top motor,
    # taking into account the previous angle
    global prevTheta4
    angleDiff = theta_4 - prevTheta4
    if angleDiff != 0:
        # Make the commandString
        # commandString = "A"
        t4 = 0
        for x in range(0, abs(math.floor(angleDiff / 10))):
            if angleDiff > 0:
                commandString += ",0,{:.0f},1000".format(prevTheta4 + 10 * (t4 + 1))
            elif angleDiff < 0:
                commandString += ",0,{:.0f},1000".format(prevTheta4 - 10 * t4)
            t4 += 1
        if angleDiff - 10 * t4 != 0:
            commandString += ",0,{:.2f},1000".format(theta_4)
        # output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta4 = theta_4  # Update prevTheta4

    # Make the commandString for PEN2 (theta_3), i.e., the second motor from the top,
    # taking into account the previous angle
    global prevTheta3
    angleDiff = theta_3 - prevTheta3
    if angleDiff != 0:
        # Make the commandString
        # commandString = "A"
        t3 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",1,{:.0f},1000".format(prevTheta3 + 5 * (t3 + 1))
            elif angleDiff < 0:
                commandString += ",1,{:.0f},1000".format(prevTheta3 - 5 * t3)
            t3 += 1
        if angleDiff - 5 * t3 != 0:
            commandString += ",1,{:.2f},1000".format(theta_3)
        # output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta3 = theta_3  # Update prevTheta3

    # Make the commandString for PEN4 (theta_1), i.e., the bottom motor,
    # taking into account the previous angle
    global prevTheta1
    angleDiff = theta_1 - prevTheta1
    if angleDiff != 0:
        # Make the commandString
        # commandString = "A"
        t1 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",3,{:.0f},1000".format(prevTheta1 + 5 * (t1 + 1))
            elif angleDiff < 0:
                commandString += ",3,{:.0f},1000".format(prevTheta1 - 5 * t1)
            t1 += 1
        if angleDiff - 5 * t1 != 0:
            commandString += ",3,{:.2f},1000".format(theta_1)
        # output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta1 = theta_1  # Update prevTheta1

    # Lastly, make the commandString for PEN3 (theta_2),
    # taking into account the previous angle
    global prevTheta2
    angleDiff = theta_2 - prevTheta2
    if angleDiff != 0:
        # Make the commandString
        # commandString = "A"
        t2 = 0
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 + 5 * (t2 + 1))
            elif angleDiff < 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 - 5 * t2)
            t2 += 1
        if angleDiff - 5 * t2 != 0:
            commandString += ",2,{:.2f},1000".format(theta_2)
        output_list.extend(constrainCommandStringLength(commandString + "\n"))
        prevTheta2 = theta_2  # Update prevTheta2

    return output_list


def drawLine(x1, y1, z1, x2, y2, z2):
    # Get the angles of the motors at the begin and end location
    th11, th21, th31, th41 = getcoords(x1, y1, z1)
    th12, th22, th32, th42 = getcoords(x2, y2, z2)

    # TODO first make code correct with begin and end coordinates, then look for maybe adding an intermediate coordinate
    # # Get intermediate angles if the distance between begin and end location is bigger than 5
    # th13, th23, th33, th43 = 0, 0, 0, 0
    # if math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2) > 5:
    #     th13, th23, th33, th43 = getcoords(abs((x1+x2)/2), abs((y1+y2)/2), abs((z1+z2)/2))

    # TODO
    #  1. Make output_list for motor to move to the first position (Done?)
    #  2. Check whether angle of motor changes when going to new position
    #       a. If so, make commandString for this motor (Done)
    #       b. Then check with other motors and make new commandString of these commandStrings combined
    #       c. Check if they make sense using FK, i.e., the pen still touches the table
    #  3. Add commandStrings of end position to output_list

    # TODO probably update the make_list or make a new method, because it keeps the previous position in mind when
    #  going to multiple positions in one run
    output_list = make_list(th11, th21, th31, th41)

    # Get commandStrings for motors that change their angles
    pre_output_list = []
    if th11 != th12:
        pre_output_list.append(singleMotorCommandString(th12, 3))
    if th21 != th22:
        pre_output_list.append(singleMotorCommandString(th22, 2))
    if th31 != th32:
        pre_output_list.append(singleMotorCommandString(th32, 1))
    if th41 != th42:
        pre_output_list.append(singleMotorCommandString(th42, 0))

    # TODO make commandStrings for moving the motors "simultaneously" using the commandStrings from the pre_output_list


def makeListPerMotor(theta1, theta2, theta3, theta4):
    pass


def singleMotorCommandString(theta, motorID):
    """
    Create commandString for a single motor with ID={0: theta4(PEN1), 1: theta3(PEN2), 2: theta2(PEN3), 3: theta1(PEN4)}

    Parameters
    ----------
        theta : float
            The angle of the motor in degrees
        motorID : int
            ID is an integer with value 0, 1, 2 or 3, where 0 belongs to theta4, 1 to theta3, 2 to theta2, 3 to theta1

    Returns a commandString if the angle is different from the previous angle and an empty string otherwise
    """
    # Get previous angle of the motor
    prevTheta = getPrevTheta(motorID)

    # Make commandString for the motor
    angleDiff = theta - prevTheta
    if angleDiff != 0:
        # Make the commandString
        commandString = "A"
        k = 0
        for x in range(0, abs(math.floor(angleDiff / 10))):
            if angleDiff > 0:
                commandString += ",{},{:.0f},1000".format(motorID, prevTheta + 10 * (k + 1))
            elif angleDiff < 0:
                commandString += ",{},{:.0f},1000".format(motorID, prevTheta - 10 * k)
            k += 1
        if angleDiff - 10 * k != 0:
            commandString += ",{},{:.2f},1000".format(motorID, theta)
        commandString += "\n"

        # Update previous angle of the motor
        updatePrevTheta(theta, motorID)

        return commandString
    return ""


def getPrevTheta(ID):
    """ Get previous angle of the motor given ID """
    global prevTheta1, prevTheta2, prevTheta3, prevTheta4
    switch = {
        0: prevTheta4,
        1: prevTheta3,
        2: prevTheta2,
        3: prevTheta1,
    }
    return switch.get(ID)


def updatePrevTheta(theta, ID):
    """ Update prevTheta of motor with ID to theta """
    global prevTheta1, prevTheta2, prevTheta3, prevTheta4
    if ID == 0:
        prevTheta4 = theta
    elif ID == 1:
        prevTheta3 = theta
    elif ID == 2:
        prevTheta2 = theta
    elif ID == 3:
        prevTheta1 = theta


def constrainCommandStringLength(commandString):
    """ If the commandString is longer than 100 characters, cut them up into commandStrings with a max length of 100

    Parameters
    ----------
        commandString : String
            complete commandString of all movements
    """
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

    return commandStringList


def move_kinematics(player):
    if player == 'X':
        pass
    elif player == 'O':
        pass


if __name__ == '__main__':
    # Formatting is getcoords(x, y, z)
    theta1, theta2, theta3, theta4 = getcoords(-10, 20, 1)
    print("Calculating position given the angles of the inverse kinematics...")
    print(FK.calc_position(theta1, theta2, theta3, theta4))
    # Apply offset
    theta2 -= 25
    theta3 -= 50
    # Make list of commandStrings
    output = make_list(theta1, theta2, theta3, theta4)
    # print(output)
    for x in output:
       print("sending", x, end="")
