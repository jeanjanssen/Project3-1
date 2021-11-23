import math

l1 = 20.1
l2 = 13.4
l3 = 12.1
l4 = 12.5       # or 12.8?
l_pen = 6.0

TABLE_Z = 21.1


def calc_current_position(cur_angle1, cur_angle2, cur_angle3, cur_angle4):
    # Converting degrees to radians
    rad1 = cur_angle1 * math.pi / 180
    rad2 = cur_angle2 * math.pi / 180
    rad23 = (cur_angle2 + cur_angle3) * math.pi / 180
    rad234 = (cur_angle2 + cur_angle3 + cur_angle4) * math.pi / 180
    rad234pen = (cur_angle2 + cur_angle3 + cur_angle4 + 90) * math.pi / 180

    # Calculating the coordinates
    cur_y = l2 * math.sin(rad2) + l3 * math.sin(rad23) + l4 * math.sin(rad234)
    cur_z = l2 * math.cos(rad2) + l3 * math.cos(rad23) + l4 * math.cos(rad234)

    # Add pen to y & z
    cur_y += l_pen * math.sin(rad234pen)
    cur_z += l_pen * math.cos(rad234pen)

    cur_z += l1

    # Calculate x & y given the angle of the bottom motor
    cur_x = cur_y * math.sin(rad1)
    cur_y = cur_y * math.cos(rad1)

    return cur_x, cur_y, cur_z


def calc_goal_position(goal_angle1, goal_angle2, goal_angle3, goal_angle4):
    # Converting degrees to radians
    rad1 = goal_angle1 * math.pi / 180
    rad2 = goal_angle2 * math.pi / 180
    rad23 = (goal_angle2 + goal_angle3) * math.pi / 180
    rad234 = (goal_angle2 + goal_angle3 + goal_angle4) * math.pi / 180
    rad234pen = (goal_angle2 + goal_angle3 + goal_angle4 + 90) * math.pi / 180

    # Calculating the coordinates
    goal_y = l2 * math.sin(rad2) + l3 * math.sin(rad23) + l4 * math.sin(rad234)
    goal_z = l2 * math.cos(rad2) + l3 * math.cos(rad23) + l4 * math.cos(rad234)

    # Add pen to y & z
    goal_y += l_pen * math.sin(rad234pen)
    goal_z += l_pen * math.cos(rad234pen)

    goal_z += l1

    # Calculate x & y given the angle of the bottom motor
    goal_x = goal_y * math.sin(rad1)
    goal_y = goal_y * math.cos(rad1)

    return goal_x, goal_y, goal_z


def collision_check(cur_x, cur_y, cur_z, goal_x, goal_y, goal_z):

    # Trajectory is cur_z + var * dz
    # Calculate where cur_z + var * dz = TABLE_Z
    if cur_z - TABLE_Z >= 0 and goal_z - TABLE_Z >= 0:
        print("no collision")
    else:
        print("collision possible")
        dx = goal_x - cur_x
        dy = goal_y - cur_y
        dz = goal_z - cur_z

        var = (TABLE_Z - cur_z) / dz

        x_on_table_height = cur_x + var * dx
        y_on_table_height = cur_y + var * dy

        # TODO:
        #  check whether these x and y values are within the range of the table
        #  if so, first move up arm until above table


if __name__ == '__main__':
    theta_1 = 0.0
    theta_2 = 45.0
    theta_3 = 45.0
    theta_4 = 0.0

    cur_x, cur_y, cur_z = calc_current_position(theta_1, theta_2, theta_3, theta_4)
    print(cur_x, cur_y, cur_z)

    theta_1g = 0.0
    theta_2g = 45.0
    theta_3g = 45.0
    theta_4g = 0.0

    goal_x, goal_y, goal_z = calc_goal_position(theta_1g, theta_2g, theta_3g, theta_4g)

    collision_check(cur_x, cur_y, cur_z, goal_x, goal_y, goal_z)
