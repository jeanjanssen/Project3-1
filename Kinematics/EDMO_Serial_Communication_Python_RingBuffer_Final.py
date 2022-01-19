import serial
from Kinematics import IK


# Initialize serial communication variables
ser = serial.Serial('/dev/tty.usbmodem112301', 57600)  # select com-port and the serial com baud rate
ser.flushInput()  # empty the serial buffer
ser_input = []  # emtpy the serial input array
current_time = 0
prev_time = 0
interval = 0.5  # serial read update time

# Example commands to drive the motors
commandStringStop = 'S,0,0,0,1,0,0,2,0,0,3,0,2000\n'  # Stop command since ID = S
# CommandString to move the arm up straight
commandStringActivateMotors = 'A,0,0,100,1,-45,100,2,-25,100,3,0,2000\n'


# Function sending data from the PC to the Arduino
def sendData(commandString):
    print("Sending command to arduino:", commandString)
    ser.write(commandString.encode())

    # Demonstration of drawing:
    demonstrate = False
    if demonstrate:
        y = 22.5
        theta3 = 95 if y <= 25 else 50
        # output_list = IK.drawLine(2.5, y, 2.5, 27.5, theta3, returnCommandString=True, shortStrings=False)
        output_list = IK.drawPlus(2.5, y, 2.5, y-5, theta3, shortStrings=False)
        # output_list = IK.drawBox(0, y, 5, y, theta3, shortStrings=False)

        # Sending the commandStrings
        for output in output_list:
            print("sending", output, end="")
            ser.write(output.encode())


# Send commandString to power all the motors in a vertical position
sendData(commandStringActivateMotors)
