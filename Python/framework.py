import tkinter as tk
from tkinter import HORIZONTAL, NW

from PIL import Image, ImageTk

turn = "Your turn"


def start_game():
    start_screen.destroy()
    game_screen = tk.Tk()
    game_screen.title('Tic Tac Toe vs. robot arm')
    game_screen.configure(background='#a6c3e5')
    game_screen.geometry("500x600")

    title2 = tk.Text(game_screen, height=1, width=300, font=("Arial", 40), bg='#a6c3e5', pady=20,
                     highlightbackground="#a6c3e5")
    title2.tag_configure("center", justify="center")
    title2.insert(1.0, turn)
    title2.configure(state='disabled')
    title2.tag_add("center", "1.0", "end")
    title2.pack()

    canvas = tk.Canvas(width=400, height=400, bg='#a6c3e5', highlightbackground='#a6c3e5')
    canvas.place(x=50, y=175)
    org_tb_image = Image.open("Tic Tac Toe Board.gif")
    rtb_image = org_tb_image.resize((400, 400), Image.ANTIALIAS)
    tb_image = ImageTk.PhotoImage(rtb_image)
    canvas.create_image(0, 0, image=tb_image, anchor=NW)
    tk.mainloop()


start_screen = tk.Tk()
start_screen.title('Tic Tac Toe vs. robot arm')
start_screen.configure(background='#a6c3e5')
start_screen.geometry("750x500")

Title = tk.Text(start_screen, height=1, width=450, font=("Arial", 40), bg='#a6c3e5', pady=30,
                highlightbackground="#a6c3e5")
Title.tag_configure("center", justify="center")
Title.insert(1.0, "Tic Tac Toe vs a robot arm")
Title.configure(state='disabled')
Title.tag_add("center", "1.0", "end")
Title.pack()

Text1 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5', pady=10,
                highlightbackground='#a6c3e5')
Text1.tag_configure("center", justify="center")
Text1.insert(1.0, "First move for:")
Text1.configure(state='disabled')
Text1.tag_add("center", "1.0", "end")
Text1.pack()

tk.Radiobutton(start_screen, text="Robot", justify="center", variable="v", value=1, pady=5, bg='#a6c3e5',
               font=("Arial", 24,), foreground='#a6c3e5').pack()

tk.Radiobutton(start_screen, text="Player", justify="center", variable="v", value=2, pady=5, bg='#a6c3e5',
               font=("Arial", 24), fg="#000000").pack()

ORG_PG_Image = Image.open("Play_game_button.gif")
RPG_Image = ORG_PG_Image.resize((200, 100), Image.ANTIALIAS)
PG_Image = ImageTk.PhotoImage(RPG_Image)

PG_button = tk.Button(start_screen, command=start_game, image=PG_Image, width=200, height=100, bd=0,
                      highlightbackground='#a6c3e5')
PG_button.pack(pady=10)

Text2 = tk.Text(start_screen, height=1, width=100, font=("Arial", 24), bg='#a6c3e5',
                pady=15, highlightbackground='#a6c3e5')
Text2.tag_configure("center", justify="center")
Text2.insert(1.0, "Difficulty level:")
Text2.configure(state='disabled')
Text2.tag_add("center", "1.0", "end")
Text2.pack()
Slider = tk.Scale(start_screen, from_=0, to=100, orient=HORIZONTAL, length=400, bg='#a6c3e5').place(x=175, y=425)
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

    State_start(state)

"""

