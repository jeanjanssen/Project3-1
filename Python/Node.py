class Node:

    board = []
    parent = []
    children = []


    def __init__(self, board):
        self
        self.board = board

    def getBoard(self):
        return self.board

    def getParent(self):
        return self.parent

    def setParent(self,parent):
        self.parent = parent

    def getChildren(self):
        return self.children

    def addChild(self, child):
        child.setParent(self)
        self.children.append(child)