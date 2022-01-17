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

# CommandString to return the robotic arm to an up straight position
RETURN_COMMANDSTRING = "A,0,-20,1000,1,-45,0,2,-25,0,3,0,0\n"
MAX_LENGTH = 100  # Maximum length of commandString (100 is consistent with arduino code! Don't enter higher values!)


def getAngles():
    """ Returns prevTheta1 (angle PEN4), prevTheta2 (angle PEN3), prevTheta3 (angle PEN2), prevTheta4 (angle PEN1) """
    return prevTheta1, prevTheta2, prevTheta3, prevTheta4


def getcoords(px, py, pz, theta_3):
    """ Calculates the angles for the motors given the desired end-effector location (px, py, pz)

    Parameters
    ----------
        px : float
            The desired x-coordinate location of the end-effector
        py : float
            The desired y-coordinate location of the end-effector
        pz : float
            The desired z-coordinate location of the end-effector.
        theta_3 : float
            Angle of motor (PEN2) in degrees

    Returns theta_1, theta_2, theta_3, theta_4, i.e., the calculated angles for the motors
    """
    # px and py are the desired points of the end-effector

    # theta_3 should be (see e.g. in framework.py):
    #   * 95 (degrees) if the start coordinate py of a line or position is < 25
    #   * 50 (degrees) if the start coordinate py of a line or position is >= 25
    theta_3 = min(max(10, theta_3), 100)  # theta_3 = [10,100]
    theta_3 = deg2rad(theta_3)  # convert to radians for calculations

    # Calculate theta_1
    theta_1 = math.atan2(px, py)
    theta_1 = rad2deg(theta_1)
    theta_1 = min(max(-45, theta_1), 45)  # theta_1 = [-45, 45]

    # Calculate length of robot arm into the board given px and py
    l_xy = math.sqrt((px ** 2) + (py ** 2))

    # Calculate lengths of the sides (la, lb & lc) of triangle ABC
    la = getLengthTheta2Theta4(theta_3, l2, l3)
    lb = l4
    lc = math.sqrt((l_xy ** 2) + (pz ** 2))  # Length from theta_2's joint to end-effector

    # Calculate angles of triangle ABC. (Only theta_b & theta_c, because theta_a not needed for further calculations)
    theta_b = math.acos((la ** 2 + lc ** 2 - lb ** 2) / (2 * la * lc))
    theta_c = math.acos((la ** 2 + lb ** 2 - lc ** 2) / (2 * la * lb))

    # Define the lengths of the sides (ld, le & lf) of triangle DEF
    ld = l2
    le = l3
    lf = la

    # Calculate angles of triangle DEF. (Only theta_d and theta_e, because theta_f = theta_3)
    theta_d = math.acos((le ** 2 + lf ** 2 - ld ** 2) / (2 * le * lf))
    theta_e = math.acos((ld ** 2 + lf ** 2 - le ** 2) / (2 * ld * lf))

    # Calculate theta_4
    theta_4 = math.pi - (theta_d + theta_c)
    theta_4 = rad2deg(theta_4)
    theta_4 -= 24.0  # Compensation for the pen (TODO 24, 25 or 26)
    theta_4 = min(max(-90, theta_4), 90)  # theta_4 = [-90,90]

    # Calculate theta_2
    theta_2 = theta_e + theta_b + math.atan(pz / l_xy)
    theta_2 = rad2deg(theta_2)
    theta_2 = 90 - theta_2
    theta_2 = min(max(-20, theta_2), 70)  # theta_2 = [-20,70]

    theta_3 = rad2deg(theta_3)  # convert back to degrees

    return theta_1, theta_2, theta_3, theta_4


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

    # The motors move in the order:
    #       -> theta_4 (PEN1), i.e., the top motor
    #       -> theta_3 (PEN2)
    #       -> theta_1 (PEN4), i.e., the bottom motor
    #       -> theta_2 (PEN3)

    # Initialize commandString
    commandString = "A"

    # First, make commandString for PEN1 (theta_4), i.e., the top motor, taking into account the previous angle
    global prevTheta4
    angleDiff4 = theta_4 - prevTheta4
    if angleDiff4 != 0:  # Then make commandString
        t4 = 0
        for x in range(0, abs(math.floor(angleDiff4 / 10))):
            if angleDiff4 > 0:
                commandString += ",0,{:.0f},1000".format(prevTheta4 + 10 * (t4 + 1))
            elif angleDiff4 < 0:
                commandString += ",0,{:.0f},1000".format(prevTheta4 - 10 * t4)
            t4 += 1
        if angleDiff4 - 10 * t4 != 0:
            commandString += ",0,{:.2f},1000".format(theta_4)
        prevTheta4 = theta_4  # Update prevTheta4

    # Make commandString for PEN2 (theta_3), i.e., the second motor from the top, taking into account the previous angle
    global prevTheta3
    angleDiff3 = theta_3 - prevTheta3
    if angleDiff3 != 0:  # Then make commandString
        t3 = 0
        for x in range(0, abs(math.floor(angleDiff3 / 10))):
            if angleDiff3 > 0:
                commandString += ",1,{:.0f},1000".format(prevTheta3 + 10 * (t3 + 1))
            elif angleDiff3 < 0:
                commandString += ",1,{:.0f},1000".format(prevTheta3 - 10 * t3)
            t3 += 1
        if angleDiff3 - 10 * t3 != 0:
            commandString += ",1,{:.2f},1000".format(theta_3)
        prevTheta3 = theta_3  # Update prevTheta3

    # Make commandString for PEN4 (theta_1), i.e., the bottom motor, taking into account the previous angle
    global prevTheta1
    angleDiff1 = theta_1 - prevTheta1
    if angleDiff1 != 0:  # Then make commandString
        t1 = 0
        for x in range(0, abs(math.floor(angleDiff1 / 10))):
            if angleDiff1 > 0:
                commandString += ",3,{:.0f},1000".format(prevTheta1 + 10 * (t1 + 1))
            elif angleDiff1 < 0:
                commandString += ",3,{:.0f},1000".format(prevTheta1 - 10 * t1)
            t1 += 1
        if angleDiff1 - 10 * t1 != 0:
            commandString += ",3,{:.2f},1000".format(theta_1)
        prevTheta1 = theta_1  # Update prevTheta1

    # Lastly, make commandString for PEN3 (theta_2), taking into account the previous angle
    global prevTheta2
    angleDiff2 = theta_2 - prevTheta2
    if angleDiff2 != 0:  # Then make commandString
        t2 = 0
        for x in range(0, abs(math.floor(angleDiff2 / 10))):
            if angleDiff2 > 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 + 10 * (t2 + 1))
            elif angleDiff2 < 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 - 10 * t2)
            t2 += 1
        if angleDiff2 - 10 * t2 != 0:
            commandString += ",2,{:.2f},1000".format(theta_2)
        prevTheta2 = theta_2  # Update prevTheta2

    # Return list with commandStrings if one of the thetas changed, else return an empty list
    if angleDiff4 != 0 or angleDiff3 != 0 or angleDiff1 != 0 or angleDiff2 != 0:
        return constrainCommandStringLength(commandString + "\n")
    else:
        return []


def drawLine(x1, y1, z1, x2, y2, z2, theta_3, returnCommandString=True):
    # Test to show the distance between the coordinates
    length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    print("Length between points =", length)

    steps = 1

    # Get the angles of the motors at the begin and end location
    th11, th21, th31, th41 = getcoords(x1, y1, z1, theta_3)
    th12, th22, th32, th42 = getcoords(x2, y2, z2, theta_3)

    # # TODO smoothing the movement using steps?
    # print(abs(th11 - th12))
    # print(abs(th21 - th22))
    # print(abs(th31 - th32))
    # print(abs(th41 - th42))
    #
    # Get number of steps
    # steps = 0
    # new_step = int(ceil(abs(th11 - th12) / 10))
    # steps = max(steps, new_step)
    # new_step = int(ceil(abs(th21 - th22) / 10))
    # steps = max(steps, new_step)
    # new_step = int(ceil(abs(th31 - th32) / 10))
    # steps = max(steps, new_step)
    # new_step = int(ceil(abs(th41 - th42) / 10))
    # steps = max(steps, new_step)
    # print("steps =", steps)

    print("Thetas start position:\nTheta1 =", th11, "\nTheta2 =", th21, "\nTheta3 =", th31, "\nTheta4 =", th41, "\n")
    print("Thetas end position:\nTheta1 =", th12, "\nTheta2 =", th22, "\nTheta3 =", th32, "\nTheta4 =", th42, "\n")

    print(FK.calc_position(th11, th21, th31, th41))
    # print(FK.calc_position((th11+th12)/2, (th21+th22)/2, (th31+th32)/2, (th41+th42)/2))
    print(FK.calc_position(th12, th22, th32, th42))
    print()

    # Applying offsets
    th21, th31 = applyOffset(th21, th31)
    th22, th32 = applyOffset(th22, th32)

    # Initialise output list
    output_list = []

    # commandString to move to begin of line
    commandString = make_list(th11, th21, th31, th41)
    output_list.extend(commandString)

    # Add intermediate steps
    for i in range(1, steps):
        th1Temp, th2Temp, th3Temp, th4Temp = getcoords(x1 + (x2 - x1) * i / steps, y1 + (y2 - y1) * i / steps, z1)
        th2Temp, th3Temp = applyOffset(th2Temp, th3Temp)

        commandString = "A"
        flag = False
        if th11 != th1Temp:  # Bottom motor (PEN4)
            commandString += ",3,{:.2f},1000".format(th1Temp)
            flag = True
        if th41 != th4Temp:  # Top motor (PEN1)
            if flag:
                commandString += ",0,{:.2f},0".format(th4Temp)
            else:
                commandString += ",0,{:.2f},1000".format(th4Temp)
                flag = True
        if th31 != th3Temp:  # Third motor (PEN2)
            if flag:
                commandString += ",1,{:.2f},0".format(th3Temp)
            else:
                commandString += ",1,{:.2f},1000".format(th3Temp)
                flag = True
        if th21 != th2Temp:  # Second motor (PEN3)
            if flag:
                commandString += ",2,{:.2f},0".format(th2Temp)
            else:
                commandString += ",2,{:.2f},1000".format(th2Temp)
        commandString += "\n"
        output_list.extend(constrainCommandStringLength(commandString))

    # TODO check if steps is correctly implemented here
    # add commandString for middle coordinate
    # commandString = "A"
    # for i in range(1, steps):
    #     flag = False
    #     if th11 != th12:  # Bottom motor (PEN4)
    #         # commandString += ",3,{:.2f},0".format((th11 + th12) / 2)
    #         commandString += ",3,{:.2f},1000".format(th11 + (th12 - th11) * i / steps)
    #         flag = True
    #     if th41 != th42:  # Top motor (PEN1)
    #         # commandString += ",0,{:.2f},0".format((th41 + th42) / 2)
    #         if flag:
    #             commandString += ",0,{:.2f},0".format(th41 + (th42 - th41) * i / steps)
    #         else:
    #             commandString += ",0,{:.2f},1000".format(th41 + (th42 - th41) * i / steps)
    #             flag = True
    #     if th31 != th32:  # Third motor (PEN2)
    #         # commandString += ",1,{:.2f},0".format((th31 + th32) / 2)
    #         if flag:
    #             commandString += ",1,{:.2f},0".format(th31 + (th32 - th31) * i / steps)
    #         else:
    #             commandString += ",1,{:.2f},1000".format(th31 + (th32 - th31) * i / steps)
    #             flag = True
    #     if th21 != th22:  # Second motor (PEN3)
    #         # commandString += ",2,{:.2f},0".format((th21 + th22) / 2)
    #         if flag:
    #             commandString += ",2,{:.2f},0".format(th21 + (th22 - th21) * i / steps)
    #         else:
    #             commandString += ",2,{:.2f},1000".format(th21 + (th22 - th21) * i / steps)
    #             flag = True

    # add commandString for end position
    commandString = "A"
    flag = False  # to determine when to add a bigger delay
    if th11 != th12:  # Bottom motor (PEN4)
        commandString += ",3,{:.2f},1000".format(th12)
        flag = True
    if th41 != th42:  # Top motor (PEN1)
        if flag:
            commandString += ",0,{:.2f},0".format(th42)
        else:
            commandString += ",0,{:.2f},1000".format(th42)
            flag = True
    if th31 != th32:  # Third motor (PEN2)
        if flag:
            commandString += ",1,{:.2f},0".format(th32)
        else:
            commandString += ",1,{:.2f},1000".format(th32)
            flag = True
    if th21 != th22:  # Second motor (PEN3)
        if flag:
            commandString += ",2,{:.2f},0".format(th22)
        else:
            commandString += ",2,{:.2f},1000".format(th22)
    commandString += "\n"

    # Cut commandStrings into pieces of with a maximum of 100 characters
    output_list.extend(constrainCommandStringLength(commandString))

    # Add commandString to move it back to its starting position
    if returnCommandString:
        output_list.append(RETURN_COMMANDSTRING)

    for o in output_list:
        print(o, end="")

    return output_list


def drawPlus(x1, y1, z1, x2, y2, z2, theta_3):
    # List with commandString(s) to draw the first line
    list1 = drawLine(x1, y1, z1, x2, y2, z2, theta_3)

    # Determine whether the second line has to be horizontal or vertical and create these commandStrings.
    if x1 == x2:  # Vertical case
        length = abs(y2 - y1)
        y = (y1 + y2) / 2
        x_left = x1 - length / 2
        x_right = x1 + length / 2
        # Make commandString(s) for horizontal line
        list1.extend(drawLine(x_left, y, z1, x_right, y, z2, theta_3))

    elif y1 == y2:  # Horizontal case
        length = abs(x2 - x1)
        x = (x1 + x2) / 2
        y_bot = y1 - length / 2
        y_top = y1 + length / 2
        # Make commandString(s) for vertical line
        list1.extend(drawLine(x, y_top, z1, x, y_bot, z2, theta_3))

    # Add commandString to return the robot arm to a vertical position
    list1.extend(RETURN_COMMANDSTRING)

    return list1


def drawBox(x1, y1, z1, x2, y2, z2, theta3):
    # Give coordinates for the top line of the box from left to right!!!

    # Make sure the line is horizontal
    if y2 != y1:
        y2 = y1

    # Initialize output_list with commandString(s) to move to the first coordinate
    th1s, th2s, th3s, th4s = getcoords(x1, y1, z1, theta3)
    th2s, th3s = applyOffset(th2s, th3s)  # Apply offset
    output_list = make_list(th1s, th2s, th3s, th4s)

    prints = True
    if prints:
        for output in output_list:
            print(output)

    # Initialize variables for loop
    xs = x1, ys = y1, zs = z1  # Start coordinates of line
    xe = x2, ye = y2, ze = z2  # End coordinates of line
    length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)  # Length of line

    # Create commandStrings to draw boxes
    commandString = "A"
    for i in range(4):
        # Get thetas of line
        th1s, th2s, th3s, th4s = getcoords(xs, ys, zs, theta3)
        th1e, th2e, th3e, th4e = getcoords(xe, ye, ze, theta3)

        # Apply offset
        th2s, th3s = applyOffset(th2s, th3s)
        th2e, th3e = applyOffset(th2e, th3e)

        # Create commandString with delay of 2 seconds (2000 milliseconds)
        flag = False
        if th1s != th1e:  # Bottom motor (PEN4)
            commandString += ",3,{:.2f},2000".format(th1e)
            flag = True
        if th4s != th4e:  # Top motor (PEN1)
            if flag:
                commandString += ",0,{:.2f},0".format(th4e)
            else:
                commandString += ",0,{:.2f},2000".format(th4e)
                flag = True
        if th3s != th3e:  # Third motor (PEN2)
            if flag:
                commandString += ",1,{:.2f},0".format(th3e)
            else:
                commandString += ",1,{:.2f},2000".format(th3e)
                flag = True
        if th2s != th2e:  # Second motor (PEN3)
            if flag:
                commandString += ",2,{:.2f},0".format(th2e)
            else:
                commandString += ",2,{:.2f},2000".format(th2e)

        # Endpoint becomes startpoint of next line
        xs = xe, ys = ye, zs = ze
        # Update new endpoints
        if i == 0:
            # New end is (x2, y2-len, z2)
            xe = x2
            ye = y2 - length
            ze = z2
        elif i == 1:
            # New end is (x1, y1-len, z1)
            xe = x1
            ye = y1 - length
            ze = z1
        elif i == 2:
            # New end is (x1, y1, z1)
            xe = x1
            ye = y1
            ze = z1

    # Add commandString(s) to output_list
    output_list.extend(constrainCommandStringLength(commandString + "\n"))

    # Add return commandString
    output_list.append(RETURN_COMMANDSTRING)

    return output_list


def applyOffset(theta2, theta3):
    # TODO or -55 for theta3?
    return theta2 - 25, theta3 - 50


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
        for x in range(0, abs(math.floor(angleDiff / 5))):
            if angleDiff > 0:
                commandString += ",{},{:.0f},1000".format(motorID, prevTheta + 5 * (k + 1))
            elif angleDiff < 0:
                commandString += ",{},{:.0f},1000".format(motorID, prevTheta - 5 * k)
            k += 1
        if angleDiff - 5 * k != 0:
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

    Returns a list of commandStrings of which each commandString has a maximum length of 100 characters
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
    drawLine(2.5, 22.5, 1, 2.5, 27.5, 1)
    # # Formatting is getcoords(x, y, z)
    # theta1, theta2, theta3, theta4 = getcoords(-10, 20, 1)
    # print("Calculating position given the angles of the inverse kinematics...")
    # print(FK.calc_position(theta1, theta2, theta3, theta4))
    # # Apply offset
    # theta2 -= 25
    # theta3 -= 50
    # # Make list of commandStrings
    # output = make_list(theta1, theta2, theta3, theta4)
    # # print(output)
    # for x in output:
    #    print("sending", x, end="")
