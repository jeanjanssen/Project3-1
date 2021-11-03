from Node import Node
from Edge import Edge

class GameAIDB:
    root = None
    edges = []
    nodes = []
    currentGeneration = []
    previousGeneration = []
    generationCounter = 0

    def __init__(self):
        self