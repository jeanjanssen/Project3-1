import serial
from timeit import default_timer as timer

######## INIT serial communication variables ################################
import IK
import computervision.test_player as tp

ser = serial.Serial('COM10', 57600)  # select com-port and the serial com baud rate
ser.flushInput()  # empty the serial buffer
ser_input = []  # emtpy the serial input array
current_time = 0
prev_time = 0
interval = 0.5  # serial read update time

# Example commands to drive the motors
commandString = '0,0,25,0,0,45,1000,0,0,5000\n'     # data string to send to arduino
commandString1 = '1,2,5,0,2,10,1000,2,30,2000\n'    # data string to send to arduino
commandString2 = '2,3,45,0,3,-45,1000,3,0,5000\n'   # data string to send to arduino
commandString3 = '3,2,10,0,2,0,1000,2,-10,5000\n'   # data string to send to arduino
commandString4 = '4,3,45,0,3,-45,1000,3,0,5000\n'   # data string to send to arduino
commandString5 = 'S,0,0,0,1,0,0,2,0,0,3,0,2000\n'  # S,motor,angle,delay,motor,angle,delay

# Due to the offset in two of the motors, to get the arm up straight the angles should be 0, -55, -25, 0.
# We give -20, -45, -25, 0, because this makes sure that the arm is almost up straight and does not exceed its
# boundaries taking into account that it doesn't slam into the table first.
commandString6 = 'A,0,-20,100,1,-45,100,2,-25,100,3,0,1000\n'



############################# SEND DATA ##################################
# function sending data from the PC to the Arduino
def sendData():
    print("Sending command to arduino:")
    # print(commandString)
    # ser.write(commandString.encode())
    # ser.write(commandString1.encode())
    # ser.write(commandString2.encode())
    # ser.write(commandString3.encode())
    # ser.write(commandString4.encode())
    # ser.write(commandString5.encode())
    # ser.write(commandString6.encode())

    # Code to hopefully draw an X
    # coords = tp.main()
    # for c in coords:
    #     # x = c[0], y = c[1], z = c[2], phi = c[3]
    #     output = IK.getcoords(c[1], c[0], c[2], c[3])
    #
    #     for x in output:
    #         print("sending", x, end="")
    #         ser.write(x.encode())
    #     # time.sleep(10)

    # print()
    # Formatting is IK.getcoords(x, y, z)
    output = IK.getcoords(10, 5, 40.1)
    for x in output:
        print("sending", x, end="")
        ser.write(x.encode())

    # ser.write(commandString5.encode())
    # time.sleep(30)
    # ser.flushInput()

    # ser.write(output.encode())


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
