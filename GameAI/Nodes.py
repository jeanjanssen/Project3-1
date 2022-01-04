"""
Playing Dots and Boxes in Python with AI. You play the game against artificial intelligence
with the option to choose the board size. You can also choose different plys (how deep
the search algorithm goes into the search tree). AI uses two methods of Min-Max and
Alpha-Beta Pruning to defeat you.

Author: Armando8766 from GitHub
Year: 2019
Edited by: Adele Imparato
"""

class Thing: # A class for Node related operations
    def __init__(self, currentState):
        self.Current = currentState
        self.CurrentScore = 0
        self.children = {}

    def Make(self, i, j, player): # Function for generating a child node
        self.children[(i, j)] = Thing(self.Current.Get_currentState())
        mul = 1
        if player:
            mul *= -1
        self.children[(i, j)].CurrentScore = (self.children[(i, j)].Current.action(i, j) * mul) + self.CurrentScore

    def Populate(self, i, j, Child): # Function for adding a node
        self.children[(i,j)] = Child

    def Draw(self): # function for drawing the board
        self.Current.Draw_mat()
