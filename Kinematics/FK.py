import math
import IK

l1 = 20.1   # length from the base till the first joint
l2 = 13.4
l3 = 12.1
l4 = 12.5   # or 12.8?
l_pen = 6.0 # check whether length from end effector to the tip of the pen is correct every time before using FK

TABLE_Z = 21.1


# Calculate position (other two methods can be removed if goal_z doesn't need the +1)
def calc_position(theta1, theta2, theta3, theta4):
    """
    Calculate the position of the end effector given the angles of the motors

    Parameters
    ----------
        theta1 : float
            Angle of the bottom motor (PEN4)
        theta2 : float
            Angle of the third motor (PEN3)
        theta3 : float
            Angle of the second motor (PEN2)
        theta4 : float
            Angle of the top motor (PEN1)
    """

    # Converting degrees to radians
    rad1, rad2, rad23, rad234, rad234pen = get_angles_in_radians(theta1, theta2, theta3, theta4)

    # Calculating the coordinates
    y = l2 * math.sin(rad2) + l3 * math.sin(rad23) + l4 * math.sin(rad234)
    z = l2 * math.cos(rad2) + l3 * math.cos(rad23) + l4 * math.cos(rad234)

    # Add pen to y & z
    y += l_pen * math.sin(rad234pen)
    z += l_pen * math.cos(rad234pen)

    z += l1

    # Calculate x & y given the angle of the bottom motor
    x = y * math.sin(rad1)
    y = y * math.cos(rad1)

    return x, y, z


# Convert the angles to the angles needed in radians
def get_angles_in_radians(theta1, theta2, theta3, theta4):
    rad1 = theta1 * math.pi / 180
    rad2 = theta2 * math.pi / 180
    rad23 = (theta2 + theta3) * math.pi / 180
    rad234 = (theta2 + theta3 + theta4) * math.pi / 180
    rad234pen = (theta2 + theta3 + theta4 + 90) * math.pi / 180
    return rad1, rad2, rad23, rad234, rad234pen


def collision_check(cur_x, cur_y, cur_z, goal_x, goal_y, goal_z):

    # if (cur_z - TABLE_Z) >= 0, then the pen is on or above the table
    # if (goal_z - TABLE_Z) >= 0, then the goal is on or above the table
    if cur_z - TABLE_Z >= 0 and goal_z - TABLE_Z >= 0:
        print("no collision")
    else:
        print("collision possible")

        if goal_z < TABLE_Z:
            print("goal is below table\nfinish movement on table height?")
        if cur_z < TABLE_Z:
            print("current position is below the table\nmove up arm first")

        # Trajectory is     cur_z + scalar * dz
        # Calculate where   cur_z + scalar * dz = TABLE_Z

        # Calculate slope in every direction
        dx = goal_x - cur_x
        dy = goal_y - cur_y
        dz = goal_z - cur_z

        scalar = (TABLE_Z - cur_z) / dz

        x_on_table_height = cur_x + scalar * dx
        y_on_table_height = cur_y + scalar * dy

        # table coordinates:
        # -21.2 <= x <= 21.2 (difference between left and right +- 42.5)
        #  10.0 <= y <= 40.5 (difference between top and bottom +- 30.5)

        if -21.2 <= x_on_table_height <= 21.2:
            print("arm should be moved upwards before movement to the goal position")
        if 10.0 <= y_on_table_height <= 40.5:
            print("arm should be moved upwards before movement to goal position")


if __name__ == '__main__':
    theta_1 = 0.0
    theta_2 = 45.0
    theta_3 = 45.0
    theta_4 = 0.0

    IK.getcoords(20, 10, 21.1, 69)
    theta_1, theta_2, theta_3, theta_4 = IK.getAngles()
    theta_2 += 55   # Reach of PEN2 is between 10 and 100 degrees
    theta_3 += 25   # Reach of PEN3 is between -20 and 70 degrees
    print(theta_1, theta_2, theta_3, theta_4)

    cur_x, cur_y, cur_z = calc_position(theta_1, theta_2, theta_3, theta_4)
    print(cur_x, cur_y, cur_z)

    # with the degrees below, the pen should be able to touch the table
    theta_1g = 0.0
    theta_2g = 45.0
    theta_3g = 45.0
    theta_4g = 12.0     # if this is 12.0 collision should not be possible

    goal_x, goal_y, goal_z = calc_position(theta_1g, theta_2g, theta_3g, theta_4g)
    print(goal_x, goal_y, goal_z)

    collision_check(cur_x, cur_y, cur_z, goal_x, goal_y, goal_z)
