import os
import tkinter
import tkinter as tk
from tkinter import HORIZONTAL
import numpy as np
import time

from Kinematics import IK
# from Kinematics import EDMO_Serial_Communication_Python_RingBuffer_Final
from GameAI import TTT_Minimax
from computervision.test_player import preprocesses, draw_SYMBOL, detect_SYMBOL
import cv2
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk
from computervision.gameboard import Tic, get_enemy

# from computervision.pre_processes import motion_detection
global output_list
output_list = []
global gamehistory
global player
player = 'X'
global first_move


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


def calculate_coordinates(cv_coords):
    # any grid coordinate: [x, y, width, height]
    ik_coords = []
    ik_coords.append(-((cv_coords[0] - cv_coords[2] / 2) * (42.5 / 733) - 42.5 / 2))
    ik_coords.append((cv_coords[1] + cv_coords[3] / 2) * (30.5 / 540) + 10)
    ik_coords.append(cv_coords[2] * (42.5 / 733))
    ik_coords.append(cv_coords[3] * (30.5 / 540))
    if not -21.25 < ik_coords[0] < 21.25:
        print("x-coordinate computed incorrectly: out of reach: ", ik_coords[0])
    if not 10 < ik_coords[1] < 40.5:
        print("y-coordinate computed incorrectly: out of reach: ", ik_coords[1])
    return ik_coords


"""
State machine for waiting for and making moves
begin: Start the state machine
make_move: Calculate correct move, calculate the kinematics and compute an output list
moving: Sending the next value of the output list to the arduino
wait_move: Wait for the player to make a move, checking the board the entire time
end: End the state machine, making clear that the game has finished
"""


def state_start(state, frame, gameboard):
    if state == "begin":
        # Check who starts the game
        if v.get() == "1":
            global player
            player = 'X'
            print("robot begins")
            return "make_move"
        elif v.get() == "2":
            print("player begins")
            global first_move
            first_move = True
            return "wait_move"
        else:
            print("error with v" + v.get())
    elif state == "make_move":
        print("make_move")
        # computer move is a number between 1 and 9
        global difficulty
        global computer_move
        computer_move = TTT_Minimax.determine(gameboard.squares, player, difficulty)
        # Convert the Computer Vision coordinates to coordinates the Inverse Kinematics can use.
        try:
            grid = preprocesses(frame)[2]
            cv_coords = grid[computer_move]
            coords = calculate_coordinates(cv_coords)
        except:
            pass
        print(coords)
        # coords = [10, 30]
        # Create commands to move to the desired point
        if coords[1] < 25:
            theta_3 = 95  # degrees for drawing on the first half of the table
        elif coords[1] >= 25:
            theta_3 = 50  # degrees for drawing on the second half of the table
        global output_list
        small_side = min(coords[2], coords[3])
        if player == 'X':
            output_list = IK.drawPlus(coords[0] - 0.4 * small_side, coords[1], coords[0] + 0.4 * small_side
                                      , coords[1], theta_3)
        elif player == 'O':
            output_list = IK.drawBox(coords[0] - 0.4 * small_side, coords[1] + 0.4 * small_side,
                                     coords[0] + 0.4 * small_side, coords[1] + 0.4 * small_side, theta_3)
        print(output_list)
        return "moving"
    elif state == "moving":
        # Check whether the output_list has been iterated over
        global list_index
        print("index", list_index, "out of", len(output_list))
        if list_index >= len(output_list):
            paper_cut, paper_fresh_cut, grid = preprocesses(frame)
            try:
                gameboard.make_move(computer_move, player)
                global gamehistory
                gamehistory[computer_move] = {'shape': player, 'bbox': grid[computer_move]}
            except:
                pass
            if gameboard.complete():
                return "end"
            list_index = 0
            output_list = []
            return "wait_move"
        current_time = time.time()
        command_string = output_list[list_index]
        command_arr = command_string[:-1].split(",")
        interval = int(command_arr[3])
        global next_time
        if next_time < current_time:
            # If the output_list still has unread values, send the next one to the arduino
            # EDMO_Serial_Communication_Python_RingBuffer_Final.sendData(command_string)
            list_index += 1
            next_time = current_time + interval / 1000
        return "moving"
    elif state == "wait_move":

        paper_cut, paper_thresh_cut, grid = preprocesses(frame)

        available_moves = np.delete(np.arange(9), list(gamehistory.keys()))
        for i, (x, y, w, h) in enumerate(grid):
            # gameboard.show()
            if i not in available_moves:
                continue
            # Find what is inside each free cell
            cell = paper_thresh_cut[int(y): int(y + h), int(x): int(x + w)]
            # if detect_SYMBOL(cell, player, model) is not None:
            if not first_move:
                shape = detect_SYMBOL(cell, get_enemy(player), model)
            elif first_move:
                shape = detect_SYMBOL(cell, 'O', model)
                if shape == '0':
                    shape = detect_SYMBOL(cell, 'X', model)

            # shape = detect_SYMBOL(cell, player)
            # print(shape)
            if shape != '0':
                print("detected_move", shape, "in grid", i)
                gamehistory[i] = {'shape': shape, 'bbox': (x, y, w, h)}
                gameboard.make_move(i, shape)
                gameboard.show()
                if first_move:
                    player = get_enemy(shape)
                if gameboard.complete():
                    return "end"
                return "make_move"

        return "wait_move"


"""
Initialize the second UI screen, showing the board.
Then start up and maintain the camera streaming, call the collision detection and the state machine
"""


def start_TTT_game():
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

    # Initialize important variables
    gameboard = Tic()
    global gamehistory
    gamehistory = {}
    global state
    state = "begin"
    global next_time
    next_time = 0
    global list_index
    list_index = 0
    global first_move
    first_move = False
    global model
    os.path
    model = load_model('../data/model_daniel.h5')

    # initialize camera streaming
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam'.format())
    # Stream the camera while playing the game
    print("loop started")
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

        # Run Preprocesses on the computervision
        try:
            if preprocesses(frame)[2] is None:
                pass
            paper_cut, paper_thresh_cut, grid = preprocesses(frame)
        except:
            pass
        # Run motion detection every instance of the loop
        # If any other object is detected, run the collision prevention
        """
        if motion_detection.motiondection(vcap):
            while motion_detection.motiondection(vcap):
                pass
        """

        try:
            # Draw grid wait on user
            for i, (x, y, w, h) in enumerate(grid):
                cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 2)
                if gamehistory.get(i) is not None:
                    shape = gamehistory[i]['shape']
                    paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
        except:
            pass

        # Run the methods according to a state machine
        print("state: ", state)
        state = state_start(state, frame, gameboard)

        if not key == 32:
            try:
                cv2.imshow('Tic Tac Toe game feed', paper_cut)
            except:
                cv2.imshow('Tic Tac Toe game feed', frame)
            continue

    gameboard.show()


# Open up starting window
start_screen = tk.Tk()
start_screen.title('Tic Tac Toe vs. robot arm')
start_screen.configure(background='#a6c3e5')
start_screen.geometry("750x500")

# Window title
Title = tk.Text(start_screen, height=1, width=450, font=("Arial", 40), bg='#a6c3e5', pady=30,
                highlightbackground="#a6c3e5", fg='#000000')
Title.tag_configure("center", justify="center")
Title.insert(1.0, "Tic Tac Toe vs a robot arm")
Title.configure(state='disabled')
Title.tag_add("center", "1.0", "end")
Title.pack()

# Radio buttons for deciding who moves first
Text1 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5', pady=10,
                highlightbackground='#a6c3e5', fg='#000000')
Text1.tag_configure("center", justify="center")
Text1.insert(1.0, "First move for:")
Text1.configure(state='disabled')
Text1.tag_add("center", "1.0", "end")
Text1.pack()
# Actual Radio buttons
v = tkinter.StringVar()
tk.Radiobutton(start_screen, text="Robot", justify="center", variable=v, value=1, pady=5, bg='#a6c3e5',
               font=("Arial", 24,), fg='#000000').pack()

tk.Radiobutton(start_screen, text="Human", justify="center", variable=v, value=2, pady=5, bg='#a6c3e5',
               font=("Arial", 24), fg="#000000").pack()
v.set(1)

# Play game Button
ORG_PTTT_Image = Image.open("Play_TTT_Button.gif")
RPTTT_Image = ORG_PTTT_Image.resize((190, 100), Image.ANTIALIAS)
PTTT_Image = ImageTk.PhotoImage(RPTTT_Image)

P_TTT_button = tk.Button(start_screen, command=start_TTT_game, image=PTTT_Image, width=200, height=100, bd=0,
                         highlightbackground='#a6c3e5', bg='#a6c3e5')
P_TTT_button.pack(pady=10)

# Difficulty Slider
Text2 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5',
                pady=15, highlightbackground='#a6c3e5', fg='#000000')
Text2.tag_configure("center", justify="center")
Text2.insert(1.0, "Difficulty level:")
Text2.configure(state='disabled')
Text2.tag_add("center", "1.0", "end")
Text2.pack()
slider = tk.Scale(start_screen, from_=0, to=100, orient=HORIZONTAL, length=400, bg='#a6c3e5', fg='#000000')
slider.place(x=175, y=425)
slider.set(100)
difficulty = slider.get()
tk.mainloop()
