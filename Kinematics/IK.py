import math
from numpy import *
from re import finditer
from Kinematics import FK

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 14  # length to the pen

# Previous thetas such that the arm is (almost) up straight at the start
prevTheta1 = 0.0  # PEN4, bottom motor
prevTheta2 = -25.0  # PEN3
prevTheta3 = -45.0  # PEN2
prevTheta4 = -20.0  # PEN1, top motor

# CommandString to return the robotic arm to an up straight position
MAX_LENGTH = 100  # Maximum length of commandString (100 is consistent with arduino code! Don't enter higher values!)


def getPrevThetas():
    """ Returns prevTheta1 (angle PEN4), prevTheta2 (angle PEN3), prevTheta3 (angle PEN2), prevTheta4 (angle PEN1) """
    global prevTheta1, prevTheta2, prevTheta3, prevTheta4
    return prevTheta1, prevTheta2, prevTheta3, prevTheta4


def useReturnCommandString():
    """
    Updates the prevThetas to the angles used in RETURN_COMMANDSTRING
    Returns RETURN_COMMANDSTRING
    """
    RETURN_COMMANDSTRING = "A,0,-20,2000,1,-45,0,2,-25,0,3,0,0\n"  # (35 characters)
    global prevTheta1, prevTheta2, prevTheta3, prevTheta4
    prevTheta1 = 0
    prevTheta2 = -25
    prevTheta3 = -45
    prevTheta4 = -20
    return RETURN_COMMANDSTRING


def getcoords(px, py, pz, theta_3):
    """
    Calculates the angles for the motors given the desired end-effector location (px, py, pz)

    Parameters
    ----------
        px : float
            The desired x-coordinate location of the end-effector
        py : float
            The desired y-coordinate location of the end-effector
        pz : float
            The desired z-coordinate location of the end-effector
        theta_3 : float
            Angle of motor (PEN2) in degrees

    Returns theta_1, theta_2, theta_3, theta_4, i.e., the calculated angles for the motors
    """

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


def make_list(theta_1, theta_2, theta_3, theta_4, shortStrings=False):
    """
    Makes a list of commandStrings which are to be sent to the motors

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
        for x in range(0, abs(math.floor(angleDiff2 / 5))):
            if angleDiff2 > 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 + 5 * (t2 + 1))
            elif angleDiff2 < 0:
                commandString += ",2,{:.0f},1000".format(prevTheta2 - 5 * t2)
            t2 += 1
        if angleDiff2 - 5 * t2 != 0:
            commandString += ",2,{:.2f},1000".format(theta_2)
        prevTheta2 = theta_2  # Update prevTheta2

    # Return list with commandStrings if one of the thetas changed, else return an empty list
    if angleDiff4 != 0 or angleDiff3 != 0 or angleDiff1 != 0 or angleDiff2 != 0:
        return constrainCommandStringLength(commandString + "\n", shortStrings=shortStrings)
    else:
        return []


def drawLine(x1, y1, x2, y2, theta_3, returnCommandString=True, shortStrings=False):
    """
    Makes a list of commandString to draw a line from (x1,y1) to (x2,y2)

    Parameters
    ----------
        x1 : float
            x-coordinate 1
        y1 : float
            y-coordinate 1
        x2 : float
            x-coordinate 2
        y2 : float
            y-coordinate 2
        theta_3 : float
            Angle of theta_3 in degrees
        returnCommandString : boolean
            Default is True. If True, then it includes a commandString (RETURN_COMMANDSTRING) such that the robot arm
            returns to a vertical position. Otherwise, it does not include this commandString
    """

    # TODO CLEAN PRINTS

    # TODO check z, either adjust the pen or the z-values
    # z-coordinates should always be -1
    z1 = -1
    z2 = -1

    # Get the angles of the motors at the begin and end location
    th1s, th2s, th3s, th4s = getcoords(x1, y1, z1, theta_3)
    th1e, th2e, th3e, th4e = getcoords(x2, y2, z2, theta_3)

    # Applying offsets
    th2s, th3s = applyOffset(th2s, th3s)
    th2e, th3e = applyOffset(th2e, th3e)

    # Initialise output list with commandString(s) to move to the start of the line
    output_list = make_list(th1s, th2s, th3s, th4s, shortStrings=shortStrings)

    # print("Print in drawLine() method:")
    # print("---------------------------")
    # for output in output_list:
    #     print("Go down:", output, end="")

    # add commandString for end position
    commandString = "A"
    flag = False  # to determine when to add a bigger delay
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
    # Add commandString (max 45 characters) to output_list
    output_list.append(commandString + "\n")
    # print("Draw line:", output_list[-1], end="")

    if returnCommandString:
        # Add commandString to move it back to its starting position
        output_list.append(useReturnCommandString())
        # print("Move back up:", output_list[-1], end="")
    else:
        # Update prevThetas
        global prevTheta1, prevTheta2, prevTheta3, prevTheta4
        prevTheta1 = th1e
        prevTheta2 = th2e
        prevTheta3 = th3e
        prevTheta4 = th4e

    return output_list


def drawPlus(x1, y1, x2, y2, theta_3, shortStrings=False):
    """
    Method that creates the commandStrings to draw a plus

    Parameters
    ----------
        x1 : float
            Left x-coordinate OR top x-coordinate
        y1 : float
            Left y-coordinate OR top y-coordinate
        x2 : float
            Right x-coordinate OR bottom x-coordinate
        y2 : float
            Right y-coordinate OR bottom y-coordinate
        theta_3 : float
            Angle of theta_3 in degrees

    Returns a list with commandStrings to draw a plus
    """

    # TODO CLEAN PRINTS

    # print("Print in drawPlus() method:")
    # print("---------------------------")

    # List with commandString(s) to draw the first line
    output_list = drawLine(x1, y1, x2, y2, theta_3, returnCommandString=False, shortStrings=shortStrings)

    # Get thetas from end position
    th1, th2, th3, th4 = getPrevThetas()
    # print(getPrevThetas())
    # Move up two motors
    th2up = th2 - 20
    th4up = th4 - 20

    # Make single commandString to move motors up in order: theta2 -> (theta3 ->) theta4
    move_up = singleMotorCommandString(th2up, 2, 2000)  # Second motor (PEN3)
    # TODO check whether we can remove commandString for third motor (PEN2), i.e., theta3, below
    # move_up = move_up[:-1] + singleMotorCommandString(th3up, 1, 0)[1:]  # Third motor (PEN2)
    move_up = move_up[:-1] + singleMotorCommandString(th4up, 0, 0)[1:]  # Top motor (PEN1)
    output_list.append(move_up)  # move_up has max 25 or 35 characters
    # print("Move up:", move_up)
    # print(getPrevThetas())

    # Determine whether the second line has to be horizontal or vertical and create these commandStrings.
    if x1 == x2:  # Vertical case
        length = abs(y2 - y1)
        y = (y1 + y2) / 2
        x_left = x1 - length / 2
        x_right = x1 + length / 2
        # Make commandString(s) for horizontal line
        temp_list = drawLine(x_left, y, x_right, y, theta_3, shortStrings=shortStrings)
        output_list.extend(temp_list)
        # for output in output_list:
        #     print(output, end="")
        # output_list.extend(drawLine(x_left, y, x_right, y, theta_3, shortStrings=shortStrings))
    elif y1 == y2:  # Horizontal case
        length = abs(x2 - x1)
        x = (x1 + x2) / 2
        y_bot = y1 - length / 2
        y_top = y1 + length / 2
        # Make commandString(s) for vertical line
        temp_list = drawLine(x, y_top, x, y_bot, theta_3, shortStrings=shortStrings)
        output_list.extend(temp_list)
        # for output in output_list:
        #     print(output, end="")
        # output_list.extend(drawLine(x, y_top, x, y_bot, theta_3, shortStrings=shortStrings))
    # print("---------------------------\n")

    return output_list


def drawBox(x1, y1, x2, y2, theta3, shortStrings=False):
    """
    Method that creates the commandStrings to draw a box.
    NEEDS upper left coordinate (x1,y1), upper right coordinate (x2,y2) and theta3.

    Returns a list with commandStrings to draw a box

    Parameters
    ----------
        x1 : float
            upper left x-coordinate
        y1 : float
            upper left y-coordinate
        x2 : float
            upper right x-coordinate
        y2 : float
            upper right y-coordinate
        theta3 : float
            angle of theta3 in degrees
    """

    # TODO CLEAN PRINTS

    # TODO check z, either adjust the pen or the z-values
    # z-coordinates should always be -1
    z1 = -1
    z2 = -1

    # Make sure the line is horizontal
    if y2 != y1:
        y2 = y1

    # Initialize output_list with commandString(s) to move to the first coordinate
    th1s, th2s, th3s, th4s = getcoords(x1, y1, z1, theta3)
    th2s, th3s = applyOffset(th2s, th3s)  # Apply offset
    output_list = make_list(th1s, th2s, th3s, th4s, shortStrings=shortStrings)

    # Start coordinates of line
    xs = x1
    ys = y1
    zs = z1
    # End coordinates of line
    xe = x2
    ye = y2
    ze = z2
    # Length of line
    length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

    # Create commandStrings to draw a box
    for i in range(4):
        # Get thetas of line
        th1s, th2s, th3s, th4s = getcoords(xs, ys, zs, theta3)
        th1e, th2e, th3e, th4e = getcoords(xe, ye, ze, theta3)

        # Apply offset
        th2s, th3s = applyOffset(th2s, th3s)
        th2e, th3e = applyOffset(th2e, th3e)

        # For the last movement we want to arm to move from top to bottom, because it draws better lines
        if i == 3:
            # Update previous thetas
            global prevTheta1, prevTheta2, prevTheta3, prevTheta4
            prevTheta1 = th1e
            prevTheta2 = th2e
            prevTheta3 = th3e
            prevTheta4 = th4e
            # print("Thetas before moving up\nTheta1 =", th1e, "\nTheta2 =", th2e, "\nTheta3 =", th3e, "\nTheta4 =", th4e)

            # Move up every motor with 20 degrees
            th2up = th2e - 20
            # th3up = th3e - 20  # TODO check if needed
            th4up = th4e - 20

            # Make single commandString to move motors up in order: theta2 -> (theta3 ->) theta4
            move_up = singleMotorCommandString(th2up, 2, 2000)  # Second motor (PEN3)
            # TODO check whether we can remove commandString for third motor (PEN2), i.e., theta3, below
            # move_up = move_up[:-1] + singleMotorCommandString(th3up, 1, 0)[1:]  # Third motor (PEN2)
            move_up = move_up[:-1] + singleMotorCommandString(th4up, 0, 0)[1:]  # Top motor (PEN1)
            output_list.append(move_up)  # move_up has max 25 or 35 characters
            # print("self made commandString", move_up)
            # print("Thetas for moving up\nTheta1 =", th1e, "\nTheta2 =", th2e, "\nTheta3 =", th3e, "\nTheta4 =", th4e)

            # Make robot arm move to top left coordinate
            output_list.extend(make_list(th1s, th2s, th3s, th4s, shortStrings=shortStrings))

        # Create commandString to draw line with a 2-second delay (2000 milliseconds!)
        commandString = "A"
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
        # print(commandString)
        # Add commandString (max 45 characters) to output_list
        output_list.append(commandString + "\n")

        # Endpoint becomes startpoint of next line
        xs = xe
        ys = ye
        zs = ze

        # Update new endpoints
        if i == 0:  # New end is (x2, y2-len, z2)
            xe = x2
            ye = y2 - length
            ze = z2
        elif i == 1:  # New end is (x1, y1-len, z1)
            xe = x1
            ye = y1 - length
            ze = z1
        elif i == 2:  # New start coordinate is (x1, y1, z1)
            xs = x1
            ys = y1
            zs = z1
            # End coordinate stays the same as last movement
            # # New end was (x1, y1, z1) before the last code update
            # xe = x1
            # ye = y1 - length
            # ze = z1

    # Add return commandString
    output_list.append(useReturnCommandString())

    # print("Print commandStrings in IK.drawBox() method:\n--------------------------------------------")
    # for output in output_list:
    #     print(output, end="")
    # print("--------------------------------------------")

    return output_list


def applyOffset(theta2, theta3):
    return theta2 - 25, theta3 - 50


def singleMotorCommandString(theta, motorID, delay, singleMovement=True):
    """
    Create commandString for a single motor with ID={0: theta4(PEN1), 1: theta3(PEN2), 2: theta2(PEN3), 3: theta1(PEN4)}

    Parameters
    ----------
        theta : float
            The angle of the motor in degrees
        motorID : int
            ID is an integer with value 0, 1, 2 or 3, where 0 belongs to theta4, 1 to theta3, 2 to theta2, 3 to theta1
        delay : int
            Delay of motor movement in milliseconds. (Maximum delay is 5000, i.e., 5 seconds)
        singleMovement : boolean
            Default value is True; Boolean value which determines whether the movement for the particular motor is done
            in one time or in steps of 10 degrees

    Returns a commandString if the angle is different from the previous angle and an empty string otherwise
    """
    # Get previous angle of the motor
    prevTheta = getPrevTheta(motorID)

    # Make commandString for the motor
    if singleMovement:
        updatePrevTheta(theta, motorID)
        if delay > 5000:  # Allow maximum delay of 5 seconds
            delay = 5000
        return "A,{},{:.2f},{}\n".format(motorID, theta, delay)  # (max 15 characters)
    else:
        angleDiff = theta - prevTheta
        if angleDiff != 0:
            # Make the commandString
            commandString = "A"
            k = 0
            for x in range(0, abs(math.floor(angleDiff / 10))):
                if angleDiff > 0:
                    commandString += ",{},{:.0f},{}".format(motorID, prevTheta + 10 * (k + 1), delay)
                elif angleDiff < 0:
                    commandString += ",{},{:.0f},{}".format(motorID, prevTheta - 10 * k, delay)
                k += 1
            if angleDiff - 10 * k != 0:
                commandString += ",{},{:.2f},{}".format(motorID, theta, delay)
            commandString += "\n"

            # Update previous angle of the motor
            updatePrevTheta(theta, motorID)

            return commandString

        # Return empty string if the angle doesn't differ from previous angle
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


def constrainCommandStringLength(commandString, shortStrings=False):
    """
    If the commandString is longer than 100 characters, cut them up into commandStrings with a max length of 100

    Parameters
    ----------
        commandString : String
            complete commandString of all movements

    Returns a list of commandStrings of which each commandString has a maximum length of 100 characters
    """

    # TODO: CLEAN PRINTS

    commandStringList = []
    if shortStrings:
        # print("Print in constrainCommandStringLength() method")
        # print("----------------------------------------------")
        # print("complete:", commandString, end="")

        # Get the number of commas
        numberOfIndices = commandString.count(",")

        for i in range(3, numberOfIndices, 3):
            # Update commaIndices
            commaIndices = finditer(',', commandString)
            commaIndices = [commaIndex.start() for commaIndex in commaIndices]

            # Get cutoffPoint
            cutoffPoint = commaIndices[3]

            # Split commandStrings
            commandStringList.append(commandString[0:cutoffPoint] + "\n")
            # print("cut:", commandString[0:cutoffPoint] + "\n", end="")
            commandString = "A" + commandString[cutoffPoint:]
            # print("remaining:", commandString, end="")

        # Append last commandString
        commandStringList.append(commandString)
        # print("last:", commandString, end="")
        # print("----------------------------------------------\n")

    else:
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


if __name__ == '__main__':
    ##### ONLY FOR TESTING #####
    y_start = 22.5
    theta3 = 95 if y_start < 25 else 50
    # drawLine(2.5, y_start, 2.5, 27.5, theta3)
    # output_list = drawPlus(2.5, y_start, 2.5, 27.5, theta3, shortStrings=False)
    output_list = drawBox(0, y_start, 5, y_start, theta3, shortStrings=False)

    for output in output_list:
        print(output, end="")

    # # Formatting is getcoords(x, y, z, theta_3)
    # y = 30
    # theta3 = 95 if y < 25 else 50
    # theta1, theta2, theta3, theta4 = getcoords(-10, y, 1, theta3)
    #
    # print("Calculating position given the angles of the inverse kinematics...")
    # print(FK.calc_position(theta1, theta2, theta3, theta4))
    #
    # # Apply offset
    # theta2, theta3 = applyOffset(theta2, theta3)
    #
    # # Make list of commandStrings
    # output_list = make_list(theta1, theta2, theta3, theta4)
    #
    # # Print for testing purposes
    # for output in output_list:
    #     print(output, end="")
