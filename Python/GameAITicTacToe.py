from Node import Node
from Edge import Edge
from copy import deepcopy

# Creates the game tree data structure
# each node represents a board state

class GameAITicTacToe:
    root = None
    edges = []
    nodes = []
    currentGeneration = []
    previousGeneration = []
    generationCounter = 0

    def __init__(self):
        self

    # Checks whether the element of the cell is empty or not
    # (0 is for empty, 1 is for X and 2 is for O)
    # @param elementInCell the value of the cell
    # @return True is cell is empty
    def isCellEmpty(self, elementInCell):
        if elementInCell != 0:
            return False
        else:
            return True

    def createChildren(self, parent, currentPlayer):
        board = parent.getBoard()

        for i in range(len(board)):
            for j in range(len(board[0])):

                if self.isCellEmpty(board[i][j]):
                    childBoard = deepcopy(board)
                    childBoard[i][j] = currentPlayer
                    child = Node(childBoard)
                    parent.addChild(child)
                    self.currentGeneration.append(child)
                    self.nodes.append(child)
                    edge = Edge(parent, child)
                    self.edges.append(edge)

    def getDepth(self, currentRoot):
        depth = 0

        for i in range(len(currentRoot)):
            for j in range(len(currentRoot[0])):
                if self.isCellEmpty(currentRoot[i][j]):
                    depth += 1

        return depth

    def createTree(self, currentRoot, currentPlayer):
        root = Node(currentRoot)
        self.nodes.append(root)
        self.createChildren(root, currentPlayer)

        #print('depth', self.getDepth(currentRoot))
        while self.generationCounter < self.getDepth(currentRoot):
            #print('generation counter', self.generationCounter)
            if currentPlayer == 1:
                currentPlayer = 2
            else:
                currentPlayer = 1

            #print('nr of nodes', len(self.nodes))

            self.generationCounter += 1

            self.previousGeneration = deepcopy(self.currentGeneration)
            self.currentGeneration = []
            #print('previous gene', self.previousGeneration)

            for n in self.previousGeneration:
                self.createChildren(n, currentPlayer)

            self.previousGeneration = []
