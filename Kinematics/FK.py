import math
from numpy import deg2rad

# Lengths between joints. l1 is not needed
from Kinematics import IK


# Table coordinates:
# -21.2 <= x <= 21.2 (difference between left and right +- 42.5)
#  10.0 <= y <= 40.5 (difference between top and bottom +- 30.5)

l2 = 13.4
l3 = 12.1
l4 = 12.5    # or 12.8?
l_pen = 6.0  # check whether length from end effector to the tip of the pen is correct every time before using FK

TABLE_Z = 1.0   # height from theta2 to the table


# Calculate position (other two methods can be removed if goal_z doesn't need the +1)
def calc_position(theta1, theta2, theta3, theta4):
    """ Calculate the position of the end effector given the angles of the motors

    Parameters
    ----------
        theta1 : float
            Angle of the bottom motor (PEN4) in degrees
        theta2 : float
            Angle of the third motor (PEN3) in degrees
        theta3 : float
            Angle of the second motor (PEN2) in degrees
        theta4 : float
            Angle of the top motor (PEN1) in degrees

    Returns the x, y and z coordinates
    """
    # Converting degrees to radians
    rad1, rad2, rad23, rad234, rad234pen = get_angles_in_radians(theta1, theta2, theta3, theta4)

    # Calculating the coordinates
    xy = l2 * math.sin(rad2) + l3 * math.sin(rad23) + l4 * math.sin(rad234) + l_pen * math.sin(rad234pen)
    z = l2 * math.cos(rad2) + l3 * math.cos(rad23) + l4 * math.cos(rad234) + l_pen * math.cos(rad234pen)

    # Calculate x & y given the angle of the bottom motor
    x = xy * math.sin(rad1)
    y = xy * math.cos(rad1)

    return x, y, z


def get_angles_in_radians(theta1, theta2, theta3, theta4):
    """ Convert the angles to the angles needed in radians

    Parameters
    ----------
        theta1 : float
            Angle from bottom motor (PEN4) in degrees
        theta2 : float
            Angle from third motor (PEN3) in degrees
        theta3 : float
            Angle from second motor (PEN2) in degrees
        theta4 : float
            Angle from top motor (PEN1) in degrees

    Returns the needed angles for calc_position in radians
    """
    rad1 = deg2rad(theta1)
    rad2 = deg2rad(theta2)
    rad23 = deg2rad(theta2 + theta3)
    rad234 = deg2rad(theta2 + theta3 + theta4)
    rad234pen = deg2rad(theta2 + theta3 + theta4 + 90)
    return rad1, rad2, rad23, rad234, rad234pen


if __name__ == '__main__':
    y = 20
    theta_3 = 95 if y <= 25 else 50
    theta_1, theta_2, theta_3, theta_4 = IK.getcoords(10, y, 1, theta_3)
    print("Theta1 =", theta_1, "\nTheta2 =", theta_2, "\nTheta3 =", theta_3, "\nTheta4 =", theta_4)

    cur_x, cur_y, cur_z = calc_position(theta_1, theta_2, theta_3, theta_4)
    print("(x,y,z) = (", cur_x, ",", cur_y, ",", cur_z, ")")
