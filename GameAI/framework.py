import os
import tkinter
import tkinter as tk
from tkinter import HORIZONTAL
import numpy as np
import time

from Kinematics import IK
# from Kinematics import EDMO_Serial_Communication_Python_RingBuffer_Final
from GameAI import TTT_Minimax
from computervision.pre_processes.motion_detection import video_cut
from computervision.test_player import preprocesses, draw_SYMBOL, detect_SYMBOL
import cv2
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk
from computervision.gameboard import Tic, get_enemy
import datetime
import imutils
# from computervision.pre_processes import motion_detection
global output_list
output_list = []
global gamehistory
global player
player = 'X'
global first_move
def video_cut(frame):
    cropped_image = frame[100:600, 200:900]
    return cropped_image

def motion_detection(vcap):

    baseline_frame = None
    avg_frame = None
    # loop video
    while True:
        check, frame = vcap.read()
        frame=video_cut(frame)
        # Read in frame from webcam
        text = "Unoccupied"
        frame = imutils.resize(frame, width=700)
        gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        if avg_frame is None:
            print("[INFO] starting background model...")
            avg_frame = gray2.copy().astype("float")
            continue
        cv2.accumulateWeighted(gray2, avg_frame, 0.5)
        frame_delta = cv2.absdiff(gray2, cv2.convertScaleAbs(avg_frame))
        threshdelta = cv2.adaptiveThreshold(frame_delta, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 199,6)
        threshdelta = cv2.dilate(threshdelta, None, iterations=2)
        cntsdelta = cv2.findContours(threshdelta.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cntsdelta = imutils.grab_contours(cntsdelta)
        # loop over the contours
        for c in cntsdelta:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 10:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        cv2.imshow("debug",frame)



        """   # draw the text and timestamp on the frame
        cv2.putText(frame, "board Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)
        """
        time.sleep(0.015)
        return text

def calculate_coordinates(cv_coords):
    """
    Given any box of the grid, converts the middle coordinate in the x,y plane, gotten from the computer vision,
    to coordinates the kinematics can use.
    In computer vision the (0, 0) point is the top left of the screen.
    For computer vision the (0, 0) point is the base of the robot which is at the top of the screen.

    Parameters
    ----------------
    cv_coords: array with length 4
    cv_coords[0]: x coordinate of the top right of the box
    cv_coords[1]: y coordinate of the top right of the box
    cv_coords[2]: width of the box
    cv_coords[3]: height of the box

    Returns a list with the middle coordinate of the given box in the the kinematics system.
    """
    # conversion calculations
    ik_coords = [-((cv_coords[0] - cv_coords[2] / 2) * (42.5 / 733) - 42.5 / 2),
                 (cv_coords[1] + cv_coords[3] / 2) * (30.5 / 540) + 10,
                 cv_coords[2] * (42.5 / 733),
                 cv_coords[3] * (30.5 / 540)]
    # checking whether the coordinates end up on the board
    if not -21.25 < ik_coords[0] < 21.25:
        print("x-coordinate computed incorrectly: out of reach: ", ik_coords[0])
    if not 10 < ik_coords[1] < 40.5:
        print("y-coordinate computed incorrectly: out of reach: ", ik_coords[1])
    return ik_coords


def state_start(state, frame, gameboard):
    """
    Running the game according to a state machine.

    Parameters
    -----------------------
    state: state the game is currently in
        States
        -------------------
        "begin": Start the state machine, check who has the first move
        "make_move": Calculate the move according to Game AI, calculate the neccesary movements with kinematics.
        "moving": Each iteration, send the next value to the arduino
        "wait_move": Each iteration, check if the player has made a move by checking empty spaces in the board.
        "end": End the state machine by breaking the game loop
    frame: Current frame gotten from the video streaming.
    gameboard: Current state of the board
    """
    if state == "begin":
        # Check who starts the game
        if v.get() == "1":
            global player
            player = 'O'
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
                shape = detect_SYMBOL(cell, 'X', model)
                if shape == '0':
                    shape = detect_SYMBOL(cell, 'O', model)

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
    model = load_model('/Users/stijnoverwater/Documents/GitHub/Project3-1/computervision/pre_processes/model_stino_newdata.h5')

    # initialize camera streaming
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam'.format())
    # Stream the camera while playing the game
    print("loop started")
    avg_frame = None
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
        #bool_md = motion_detection(vcap)


        # Read in frame from webcam
        text = "Unoccupied"
        frame = imutils.resize(paper_cut, width=700)
        gray2 = cv2.cvtColor(paper_cut, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        if avg_frame is None:
            print("[INFO] starting background model...")
            avg_frame = gray2.copy().astype("float")
            continue
        cv2.accumulateWeighted(gray2, avg_frame, 0.5)
        frame_delta = cv2.absdiff(gray2, cv2.convertScaleAbs(avg_frame))
        threshdelta = cv2.adaptiveThreshold(frame_delta, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                            199, 6)
        threshdelta = cv2.dilate(threshdelta, None, iterations=2)
        cntsdelta = cv2.findContours(threshdelta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntsdelta = imutils.grab_contours(cntsdelta)
        # loop over the contours
        for c in cntsdelta:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 10:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
        try:
            # Draw grid wait on user
            for i, (x, y, w, h) in enumerate(grid):
                cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 2)
                if gamehistory.get(i) is not None:
                    shape = gamehistory[i]['shape']
                    paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
        except:
            pass
        print("status:",text)
        if text == "Unoccupied":
            # Run the methods according to a state machine
            print("state: ", state)
            state = state_start(state, frame, gameboard)

        cv2.putText(paper_cut, "board Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
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
