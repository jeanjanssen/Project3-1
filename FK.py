import math

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 12.5

TABLE_Z = 21.1

cur_angle1 = 0
cur_angle2 = 0
cur_angle3 = 0
cur_angle4 = 0

cur_x = 0
cur_y = 0
cur_z = 0


def set_current_angles(new_angle1, new_angle2, new_angle3, new_angle4):
    cur_angle1 = new_angle1
    cur_angle2 = new_angle2
    cur_angle3 = new_angle3
    cur_angle4 = new_angle4


def set_current_position(new_x, new_y, new_z):
    cur_x = new_x
    cur_y = new_y
    cur_z = new_z


def get_current_position():
    return cur_x, cur_y, cur_z


def calc_current_position():
    cur_y = l2 * math.cos(cur_angle2) + l3 * math.cos(cur_angle2 + cur_angle3) + l4 * math.cos(cur_angle2 + cur_angle3 + cur_angle4)
    cur_z = l2 * math.sin(cur_angle2) + l3 * math.sin(cur_angle2 + cur_angle3) + l4 * math.sin(cur_angle2 + cur_angle3 + cur_angle4)

    cur_x = cur_y * math.cos(cur_angle1)
    cur_y = cur_y * math.sin(cur_angle1)


def calc_position_of_second_joint():
    joint1_y = l2 * math.cos(cur_angle2) + l3 * math.cos(cur_angle2 + cur_angle3)
    joint1_z = l2 * math.sin(cur_angle2) + l3 * math.sin(cur_angle2 + cur_angle3)

    joint1_x = joint1_y * math.cos(cur_angle1)
    joint1_y = joint1_y * math.sin(cur_angle1)

    return joint1_x, joint1_y, joint1_z


def calc_goal_position(theta1, theta2, theta3, theta4):
    goal_y = l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3) + l4 * math.cos(theta2 + theta3 + theta4)
    goal_z = l2 * math.sin(theta2) + l3 * math.sin(theta2 + theta3) + l4 * math.sin(theta2 + theta3 + theta4)

    goal_x = goal_y * math.cos(theta1)
    goal_y = goal_y * math.sin(theta1)

    return goal_x, goal_y, goal_z


def collision_check(theta1, theta2, theta3, theta4):
    goal_x, goal_y, goal_z = calc_goal_position(theta1, theta2, theta3, theta4)

    dx = goal_x - cur_x
    dy = goal_y - cur_y
    dz = goal_z - cur_z

    # Trajectory is cur_z + var * dz
    # Calculate where cur_z + var * dz = TABLE_Z
    if TABLE_Z - cur_z < 0 and goal_z - TABLE_Z >= 0:
        print("no collision")
    else:
        print("collision possible")
        var = (TABLE_Z - cur_z) / dz

        x_on_table_height = cur_x + var * dx
        y_on_table_height = cur_y + var * dy

        # TODO:
        #  check whether these x and y values are within the range of the table
        #  if so, first move up arm until above table

        # TODO:
        #  only part between last joint and end effector could collide (if motors are calibrated correctly)
        #  check between this joint and end effector
        j1_x, j1_y, j1_z = calc_position_of_second_joint()




