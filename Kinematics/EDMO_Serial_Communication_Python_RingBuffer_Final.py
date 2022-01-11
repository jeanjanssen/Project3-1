import serial
from timeit import default_timer as timer

######## INIT serial communication variables ################################
import IK
import FK
import computervision.test_player as tp

ser = serial.Serial('COM3', 57600)  # select com-port and the serial com baud rate
ser.flushInput()  # empty the serial buffer
ser_input = []  # emtpy the serial input array
current_time = 0
prev_time = 0
interval = 0.5  # serial read update time

# Example commands to drive the motors
# commandString = '0,0,25,0,0,45,1000,0,0,5000\n'     # data string to send to arduino
# commandString1 = '1,2,5,0,2,10,1000,2,30,2000\n'    # data string to send to arduino
# commandString2 = '2,3,45,0,3,-45,1000,3,0,5000\n'   # data string to send to arduino
# commandString3 = '3,2,10,0,2,0,1000,2,-10,5000\n'   # data string to send to arduino
# commandString4 = '4,3,45,0,3,-45,1000,3,0,5000\n'   # data string to send to arduino

# Stop command since ID = S
commandString5 = 'S,0,0,0,1,0,0,2,0,0,3,0,2000\n'  # S,motor,angle,delay,motor,angle,delay
# CommandString to move the arm up straight
commandString6 = 'A,0,0,100,1,-50,100,2,-25,100,3,0,2000\n'


############################# SEND DATA ##################################
# function sending data from the PC to the Arduino
def sendData():
    print("Sending command to arduino:")

    # Move the arm to the 0 position
    ser.write(commandString6.encode())

    # TODO this is some code for cross or circle sketching?
    # coords = tp.main()
    # for c in coords:
    #     # x = c[0], y = c[1], z = c[2], phi = c[3]
    #     # Formatting is IK.getcoords(x, y, z)
    #     theta1, theta2, theta3, theta4 = IK.getcoords(c[1], c[0], c[2], c[3])
    #     print("Calculating position given the angles of the inverse kinematics...")
    #     print(FK.calc_position(theta1, theta2, theta3, theta4))
    #
    #     # Applying offset for the motors
    #     theta2 -= 25
    #     theta3 -= 50
    #
    #     # Getting the commandStrings
    #     output = IK.make_list(theta1, theta2, theta3, theta4)
    #
    #     for x in output:
    #         print("sending", x, end="")
    #         ser.write(x.encode())
    #     # time.sleep(10)
    # print()

    ##### TESTING INVERSE KINEMATICS #####
    # Formatting is IK.getcoords(x, y, z)
    theta1, theta2, theta3, theta4 = IK.getcoords(15, 20, 1)
    print("Calculating position given the angles of the inverse kinematics...")
    print(FK.calc_position(theta1, theta2, theta3, theta4))

    # Applying offset for the motors
    theta2 -= 25
    theta3 -= 50    # TODO or 55?

    # Getting the commandStrings
    output = IK.make_list(theta1, theta2, theta3, theta4)

    # Sending the commandStrings
    for x in output:
        print("sending", x, end="")
        ser.write(x.encode())

    # Second run to see if it moves to the next position correctly as well
    second_run = False
    if second_run:
        theta1, theta2, theta3, theta4 = IK.getcoords(-10, 30, 1)
        print("Calculating position given the angles of the inverse kinematics...")
        print(FK.calc_position(theta1, theta2, theta3, theta4))

        # Applying offset for the motors
        theta2 -= 25
        theta3 -= 50

        # Getting the commandStrings
        output = IK.make_list(theta1, theta2, theta3, theta4)

        # Sending the commandStrings
        for x in output:
            print("sending", x, end="")
            ser.write(x.encode())



############################# RECEIVE DATA ##################################
# Function checking if data has been received and if yes reading it
def recData():
    print("Checking for serial input")
    # if data on the serial interface, then read it
    if ser.in_waiting > 0:
        print("Reading serial input")
        ser_input = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
        ser_input = ser_input.decode('ascii')  # decode input
        print("Data Received from Arduino:")
        print(ser_input)  # print received data


############################# MAIN ##################################
sendData()  # send drive commands once

# continuously check and read serial input
while True:
    current_time = timer()  # update current time
    # if interval is reached, check if there is a new serial input
    if current_time - prev_time >= interval:
        prev_time = current_time
        # recData()
