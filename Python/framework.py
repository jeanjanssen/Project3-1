import tkinter as tk
from tkinter import HORIZONTAL

from PIL import Image, ImageTk

r = tk.Tk()
r.title('Tic Tac Toe vs. robot arm')
r.configure(background='#85c1e9')
r.geometry("750x500")

Title = tk.Text(r, height=1, width=450, font=("Arial", 40), bg='#85c1e9', pady=30, highlightbackground="#85c1e9")
Title.tag_configure("center", justify="center")
Title.insert(1.0, "Tic Tac Toe vs a robot arm")
Title.configure(state='disabled')
Title.tag_add("center", "1.0", "end")
Title.pack()

Text1 = tk.Text(r, height=1, width=100, font=("Arial", 24), bg='#85c1e9', pady=10, highlightbackground='#85c1e9')
Text1.tag_configure("center", justify="center")
Text1.insert(1.0, "First move for:")
Text1.configure(state='disabled')
Text1.tag_add("center", "1.0", "end")
Text1.pack()

tk.Radiobutton(r, text="Robot", justify="center", variable="v", value=1, pady=5, bg='#85c1e9', font=("Arial", 24,),
               foreground='#85c1e9').pack()

tk.Radiobutton(r, text="Player", justify="center", variable="v", value=2, pady=5, bg='#85c1e9', font=("Arial", 24),
               fg="#000000").pack()


ORG_PG_Image = Image.open("Play_game_button.gif")
RPG_Image = ORG_PG_Image.resize((200, 100), Image.ANTIALIAS)
PG_Image = ImageTk.PhotoImage(RPG_Image)
PG_button = tk.Button(r, image=PG_Image, width=200, height=100, bd=0, highlightbackground='#85c1e9')
PG_button.pack(pady=10)

Text2 = tk.Text(r, height=1, width=100, font=("Arial", 24), bg='#85c1e9', pady=15, highlightbackground='#85c1e9')
Text2.tag_configure("center", justify="center")
Text2.insert(1.0, "Difficulty level:")
Text2.configure(state='disabled')
Text2.tag_add("center", "1.0", "end")
Text2.pack()
Slider = tk.Scale(r, from_=0, to=100, orient=HORIZONTAL, length=400, bg='#85c1e9').place(x=175, y=425)
r.mainloop()






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


"""
    for x in range(0, theta1, 5):
        output_list.append('S, 0, 5, 0, 1, 0, 0, 2, 0, 0, 3, 0, 0')

    for x in range(0, theta2, 5):
        output_list.append('S, 0, 0, 0, 1, 5, 0, 2, 0, 0, 3, 0, 0')

    for x in range(0, theta3, 5):
        output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 5, 0, 3, 0, 0')

    for x in range(0, theta4, 5):
        output_list.append('S, 0, 0, 0, 1, 0, 0, 2, 0, 0, 3, 5, 0')
"""
