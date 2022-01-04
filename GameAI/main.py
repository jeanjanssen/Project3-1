from Algorithm import *
from DotsNBoxes import *
from Board import *
from Nodes import *

"""
Playing Dots and Boxes in Python with AI. You play the game against artificial intelligence 
with the option to choose the board size. You can also choose different plys (how deep 
the search algorithm goes into the search tree). AI uses two methods of Min-Max and 
Alpha-Beta Pruning to defeat you.

Author: Armando8766 from GitHub
Year: 2019
Edited by: Adele Imparato
"""

def main():
    while True:

        print("\t\t!! Welcome to the game of Dots and Boxes !!\n\n Be prepared to be crushed by the power of Artificial Intelligence ... !!\n\n\
                Kidding! You totally can beat it!\n\n\n")

        x = input("Press 1 to start the game or press 2 to escape from the inevitable doom!!\n\n")
        if x == "1":
                
            Board_Xdim = int(input("\nPlease enter the number of rows for the board: \n")) * 2 + 1

            if Board_Xdim < 5:
                print("\nthe number of rows should at least be 2\n")
                exit()

            Board_Ydim = int(input("\nPlease enter the number of columns for the board: \n")) * 2 + 1

            if Board_Ydim < 5:
                print("\nthe number of columns should at least be 2\n")
                exit()

            Ply_num = int(input("\nPlease enter the number of plies used by the AI: \n"))

            if Ply_num < 2:
                print("\nThe number of plies should be higher than 1\n")
                exit()

            Match = DotsNBoxes(Board_Xdim, Board_Ydim, Ply_num)
            Match.start()
        else: 
            print ("\n\nEscape it is!")
            exit()
            
if __name__ == "__main__":
    main()
