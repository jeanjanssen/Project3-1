import os
import tkinter
import tkinter as tk
from tkinter import HORIZONTAL

from Kinematics import IK
# from Kinematics import EDMO_Serial_Communication_Python_RingBuffer_Final
from GameAI import TTT_Minimax
from computervision.test_player import preprocesses, draw_SYMBOL
import cv2
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk
from computervision.gameboard import Tic
from computervision.pre_processes import motion_detection

global list_index
list_index = 0
global output_list
output_list = []
global gamehistory
gamehistory = {}
global player
player = 'X'


def update_ui_turn(turn):
    pass

def move_coordinates(player, middleCoord):
    if player == 'X':
        getCoordsToSketchCross(middleCoord)
    if player == 'O':
        pass

def getCoordsToSketchCross(middleCoord):
    print(middleCoord)
    height_dist = 2  # TODO test which value is best
    width_dist = 2  # TODO test which value is best

    x = middleCoord[0]
    y = middleCoord[1]
    z = middleCoord[2]
    power = middleCoord[3]

    coords = []
    coord0 = (x - width_dist, y + height_dist, z, power)  # top left coord of cross
    coord1 = middleCoord
    coord2 = (x + width_dist, y - height_dist, z, power)  # bottom right coord of cross
    coord3 = (x + width_dist, y - height_dist, z + 3, power)  # position in the air before sketching second line
    coord4 = (x + width_dist, y + height_dist, z, power)  # top right coord of cross
    coord5 = middleCoord
    coord6 = (x - width_dist, y - height_dist, z, power)  # bottom left coord of cross

    coords.append(coord0)
    coords.append(coord1)
    coords.append(coord2)
    coords.append(coord3)
    coords.append(coord4)
    coords.append(coord5)
    coords.append(coord6)

    print(coords)
    return coords


def calculate_coordinates(computer_move):
    ik_coords = []
    cv_coords = gamehistory[computer_move]['bbox']
    ik_coords.append((-cv_coords.get(0)*(42.5/733) - 42.5/2))
    ik_coords.append((cv_coords.get(1)*(30.5/540) + 10))
    return ik_coords


"""
State machine for waiting for and making moves
begin: Start the state machine
make_move: Calculate correct move, calculate the kinematics and compute an output list
moving: Sending the next value of the output list to the arduino
wait_move: Wait for the player to make a move, checking the board the entire time
wait_move_first: The same as wait_move, where the symbol for the player and computer is yet to be decided by the 
                 players move.
end: End the state machine, making clear that the game has finished
"""
def state_start(state, frame, gameboard):
    if state == "begin":
        # Check who starts the game
        if v == 1:
            update_ui_turn("robot")
            global player
            player = 'X'
            return "make_move"
        if v == 2:
            update_ui_turn("player")
            return "wait_move_first"
    elif state == "make_move":
        # computer move is a number between 1 and 9
        global difficulty
        global computer_move
        computer_move = TTT_Minimax.determine(gameboard.squares, player, difficulty)
        # Convert the Computer Vision coordinates to coordinates the Inverse Kinematics can use.
        coords = calculate_coordinates(computer_move)
        # Create commands to move to the desired point
        if coords.get(1) >= 25:
            theta_3 = 95
        elif coords.get(1) < 25:
            theta_3 = 50
        global output_list
        theta_1, theta_2, theta_3, theta_4 = IK.getcoords(coords.get(0), coords.get(1), 1, theta_3)
        # Apply the offset of the motors
        theta_2, theta_3 = IK.applyOffset(theta_2, theta_3)
        output_list.extend(IK.make_list(theta_1, theta_2, theta_3, theta_4))
        # Create commands to draw the X or O
        output_list.append(IK.move_kinematics(player))
        # Create commands to move back to the idle position
        output_list.extend(IK.make_list(0, -25, -45, -20))
        return "moving"
    elif state == "moving":
        # Check whether the output_list has been iterated over
        global list_index
        if list_index > len(output_list):
            paper_cut, grid = preprocesses(frame)[0]

            if gameboard.complete():
                return "end"
            list_index = 0
            output_list = []
            return "wait_move"
        # If the output_list still has unread values, send the next one to the arduino
        command_string = output_list[list_index]
        # EDMO_Serial_Communication_Python_RingBuffer_Final.sendData(command_string)
        list_index += 1
        return "moving"
    elif state == "wait_move":
        paper_cut, grid = preprocesses(frame)[0]
        try:
            gameboard.make_move(computer_move, player)
            gamehistory[computer_move] = {'shape': player, 'bbox': grid[computer_move]}
            paper_cut = draw_SYMBOL(paper_cut, player, grid[computer_move])
            gameboard.show()
            # print(it)
        except:
            pass
        try:
            # Draw grid wait on user
            for i, (x, y, w, h) in enumerate(grid):

                cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 2)
                if gamehistory.get(i) is not None:
                    shape = gamehistory[i]['shape']
                    paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
                    gameboard.make_move(i, shape)
                    if gameboard.complete():
                        return "end"
                    return "make_move"
        except:
            # print("something wrong in corners list")
            pass
        return "wait_move"
    elif state == "wait_move_first":
        paper_cut, grid = preprocesses(frame)[0]

        try:
            # Draw grid wait on user
            for i, (x, y, w, h) in enumerate(grid):

                cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 2)
                if gamehistory.get(i) is not None:
                    shape = gamehistory[i]['shape']
                    paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
                    gameboard.make_move(i, shape)
                    player = gameboard.getenemy(shape)
                    return "make_move"

        except:
            # print("something wrong in corners list")
            pass
        return "wait_move_first"


"""
Initialize the second UI screen, showing the board.
Then start up and maintain the camera, call the collision detection and the state machine
"""


def start_TTT_game():
    print(slider.get())
    # Create Second screen with grid
    start_screen.destroy()

    """
    # Play the game with test_player
    global model
    os.path
    model = load_model('../data/model2.h5')

    # Initialize webcam feed
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam #{}'.format())
    play(vcap, difficulty)
    """

    # Frameworking for 3rd phase
    """
    game_screen = tk.Tk()
    game_screen.title('Tic Tac Toe vs. robot arm')
    game_screen.configure(background='#a6c3e5')
    game_screen.geometry("500x600")

    # Create Title indicating whose turn
    title2 = tk.Text(game_screen, height=1, width=300, font=("Arial", 40), bg='#a6c3e5', pady=20,
                     highlightbackground="#a6c3e5")
    title2.tag_configure("center", justify="center")
    if v == 1:
        title2.insert(1.0, "Robot's turn")
    elif v == 2:
        title2.insert(1.0, "Your turn")
    title2.configure(state='disabled')
    title2.tag_add("center", "1.0", "end")
    title2.pack()

    # Create canvas with grid
    canvas = tk.Canvas(width=400, height=400, bg='#a6c3e5', highlightbackground='#a6c3e5')
    canvas.place(x=50, y=175)
    org_tb_image = Image.open("Tic Tac Toe Board.gif")
    rtb_image = org_tb_image.resize((400, 400), Image.ANTIALIAS)
    tb_image = ImageTk.PhotoImage(rtb_image)
    canvas.create_image(0, 0, image=tb_image, anchor=NW)

    tk.mainloop()
    """


    # Initialize opponent (computer)
    gameboard = Tic()
    gamehistory = {}
    state = "begin"
    list_index=0
    global model
    os.path
    # model = load_model('computervision/data/model2.h5')

    # initialize camera streaming
    vcap = cv2.VideoCapture(1)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam'.format())
    # Stream the camera while playing the game
    lastframe = vcap.read()[1]
    while state != "end":
        ret, frame = vcap.read()
        key = cv2.waitKey(1) & 0xFF
        if not ret:
            print('[INFO] finished video processing')
            break

        # kill switch is q
        if key == ord('q'):
            print('[INFO] stopped video processing')
            break

        # Run motion detection every instance of the loop
        # If any other object is detected, run the collision prevention
        # video = frame + lastframe
        if motion_detection.motiondection(vcap):
            while motion_detection.motiondection(vcap):
                pass
        lastframe = frame

        # Run the methods according to a state machine
        state = state_start("begin", frame, gameboard)

        if not key == 32:
            cv2.imshow('original', frame)
            continue


def start_dots_and_boxes():
    pass


# Open up starting window
start_screen = tk.Tk()
start_screen.title('Tic Tac Toe vs. robot arm')
start_screen.configure(background='#a6c3e5')
start_screen.geometry("750x500")

# Window title
Title = tk.Text(start_screen, height=1, width=450, font=("Arial", 40), bg='#a6c3e5', pady=30,
                highlightbackground="#a6c3e5")
Title.tag_configure("center", justify="center")
Title.insert(1.0, "Tic Tac Toe vs a robot arm")
Title.configure(state='disabled')
Title.tag_add("center", "1.0", "end")
Title.pack()

# Radio buttons for deciding who moves first
Text1 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5', pady=10,
                highlightbackground='#a6c3e5')
Text1.tag_configure("center", justify="center")
Text1.insert(1.0, "First move for:")
Text1.configure(state='disabled')
Text1.tag_add("center", "1.0", "end")
Text1.pack()
# Actual Radio buttons
v = tkinter.StringVar()
tk.Radiobutton(start_screen, text="Robot", fg="black", justify="center", variable=v, value=1, pady=5, bg='#a6c3e5',
               font=("Arial", 24,), foreground='#a6c3e5').pack()

tk.Radiobutton(start_screen, text="Human", justify="center", variable=v, value=2, pady=5, bg='#a6c3e5',
               font=("Arial", 24), fg="#000000").pack()
v.set(1)

# Play game Button
ORG_PTTT_Image = Image.open("Play_TTT_Button.gif")
RPTTT_Image = ORG_PTTT_Image.resize((190, 100), Image.ANTIALIAS)
PTTT_Image = ImageTk.PhotoImage(RPTTT_Image)

P_TTT_button = tk.Button(start_screen, command=start_TTT_game, image=PTTT_Image, width=200, height=100, bd=0,
                          highlightbackground='#a6c3e5')
P_TTT_button.place(x=155, y=265)

ORG_PDB_Image = Image.open("Play_D&B_Button.gif")
RPDB_Image = ORG_PDB_Image.resize((190, 100), Image.ANTIALIAS)
PDB_Image = ImageTk.PhotoImage(RPDB_Image)
P_DG_button = tk.Button(start_screen, command=start_dots_and_boxes, image=PDB_Image, width=200, height=100, bd=0,
                        highlightbackground='#a6c3e5')
P_DG_button.place(x=395, y=265)


# Difficulty Slider
Text2 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5',
                pady=15, highlightbackground='#a6c3e5')
Text2.tag_configure("center", justify="center")
Text2.insert(1.0, "Difficulty level:")
Text2.configure(state='disabled')
Text2.tag_add("center", "1.0", "end")
Text2.place(x=-285, y=375)
slider = tk.Scale(start_screen, from_=0, to=100, orient=HORIZONTAL, length=400, bg='#a6c3e5')
slider.place(x=175, y=425)
slider.set(100)
difficulty = slider.get()
tk.mainloop()
