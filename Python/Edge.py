from Node import Node


class Edge:
    source = None
    destination = None

    def __init__(self, source, destination):
        self
        self.source = source
        self.destination = destination

    def getDestination(self):
        return self.destination

    def getSource(self):
        return self.source

    def __str__(self):
        return self.source + "" + self.destination
