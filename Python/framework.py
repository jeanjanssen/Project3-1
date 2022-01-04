import os
import tkinter
import tkinter as tk
from tkinter import HORIZONTAL, NW

# import EDMO_Serial_Communication_Python_RingBuffer_Final
import IK
from Python import Minimax
from computervision.test_player import play, preprocesses, draw_SYMBOL
import cv2
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk
from computervision.alphabeta import Tic
from computervision.pre_processes import motion_detection

list_index = 0
output_list = []
# turn = "Your turn"
gamehistory = {}
player = 'X'


# def gameFinished():

def update_ui_turn(turn):
    pass


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
        global player
        global difficulty
        computer_move = Minimax.determine(gameboard.squares, player, difficulty)
        # Calculate the coordinates and get the Inverse kinematics
        coords = calculate_coordinates(computer_move)
        global output_list
        # Create commands to move to the desired point
        output_list.append(IK.getcoords(coords.get(1), coords.get(2), coords.get(3), coords.get(4)))
        # Create commands to draw the X or O
        output_list.append(IK.move_kinematics(player))
        # Create commands to move back to the idle position
        output_list.append(IK.makelist(0, 0, 0, 0))
        return "moving"
    elif state == "moving":
        # Check whether the output_list has been iterated over
        global list_index
        if list_index > len(output_list):
            if gameboard.complete():
                return "end"
            list_index = 0
            return "wait_move"
        # If the output_list still has unread values, send the next one to the arduino
        command_string = output_list[list_index]
        # EDMO_Serial_Communication_Python_RingBuffer_Final.sendData(command_string)
        list_index += 1
        return "moving"
    elif state == "wait_move":
        if gameboard.complete():
            return "end"
        paper_cut, grid = preprocesses(frame)[0]

        try:
            # Draw grid wait on user
            for i, (x, y, w, h) in enumerate(grid):

                cv2.rectangle(paper_cut, (x, y), (x + w, y + h), (0, 0, 0), 2)
                if gamehistory.get(i) is not None:
                    shape = gamehistory[i]['shape']
                    paper_cut = draw_SYMBOL(paper_cut, shape, (x, y, w, h))
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
        except:
            # print("something wrong in corners list")
            pass
        return "wait_move_first"


"""
Initialize the second UI screen, showing the board.
Then start up and maintain the camera, call the collision detection and the state machine
"""


def start_game():
    print(slider.get())
    # Create Second screen with grid
    start_screen.destroy()

    # Play the game with test_player
    global model
    os.path
    model = load_model('../data/model2.h5')

    # Initialize webcam feed
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam #{}'.format())
    play(vcap, difficulty)

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
    vcap = cv2.VideoCapture(0)
    if not vcap.isOpened():
        raise IOError('could not get feed from cam'.format())
    # Stream the camera while playing the game
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

    
        if motion_detection.motiondection(frame):
            while motion_detection.motiondection(frame):
                pass
        

        if not key == 32:
            cv2.imshow('original', frame)
            continue

        # Run the methods according to a state machine
        # state = state_start("begin", frame, gameboard, difficulty)
    """


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
ORG_PG_Image = Image.open("Play_game_button.gif")
RPG_Image = ORG_PG_Image.resize((200, 100), Image.ANTIALIAS)
PG_Image = ImageTk.PhotoImage(RPG_Image)

PG_button = tk.Button(start_screen, command=start_game, image=PG_Image, width=200, height=100, bd=0,
                      highlightbackground='#a6c3e5')
PG_button.pack(pady=10)

# Difficulty Slider
Text2 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5',
                pady=15, highlightbackground='#a6c3e5')
Text2.tag_configure("center", justify="center")
Text2.insert(1.0, "Difficulty level:")
Text2.configure(state='disabled')
Text2.tag_add("center", "1.0", "end")
Text2.pack()
slider = tk.Scale(start_screen, from_=0, to=100, orient=HORIZONTAL, length=400, bg='#a6c3e5')
slider.place(x=175, y=425)
slider.set(100)
difficulty = slider.get()
tk.mainloop()


"""
The framework of the application using a state machine
Six states:
begin: begin the loop
make_move: calculate move and move arm to the position, whilst checking for collision
avoid: collision detected: move out of the way
wait_avoid: wait for the collision to move out of the field
wait_move: wait for the player to make a move, whilst checking for collision
end: game has finished, end the loop

state = "begin"
first_move = 0

class Status:

def State_start(state):
    if state == "begin":
        if first_move == 0:
            state = "make_move"
        elif first_move == 1:
            state = "wait_move"
    elif state == "make_move":
        if game_end:
            state == end
        else:
            if Check_collision()
                state == avoid
                last_state = make_move
            Make the move()
            if Check collision()
                state == avoid
            if game_end:
                state == end
            else:
                state == wait_move
    elif state == "avoid":
        Move_away()  (most likely to upright position)
        state == wait_avoid;
    elif state == "wait_avoid":
        if !Check_collision
            state = last_state
    elif state == "wait_move":
        if Check_collision()
            state == avoid
        else Check_board()
            if updated_board = true
                board = updated
                state = make_move
    elif state == "end":
        Move_to_start_position()
        return game
    else:
        return state

"""
