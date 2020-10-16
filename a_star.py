import heapdict
import numpy as np
import random

def reconstruct_path(cameFrom, current):
    totalPath = [current]
    while current in cameFrom:
        current = cameFrom[current]
        totalPath.append(current)
    return totalPath

# For this to work start start and goal must be the same type, be hashable and have a function called getNeighbors that returns a tuple (neighbor, weight)
def a_star(start, h, isGoal):
    openSet = heapdict.heapdict()
    openSet[start] = h(start)
    cameFrom = {}
    gScore = {start: 0}

    while len(openSet) > 0:
        _, current = openSet.peekitem()
        if isGoal(current):
            return reconstruct_path(cameFrom, current)
        openSet.pop()

        for neighbor, weight in current.getNeighbors():
            tentativeGScore = gScore[current] + weight
            if (not (neighbor in gScore)) or tentativeGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                openSet[neighbor] = tentativeGScore + h(neighbor)

    return []


def one_way_a_star(start, h, isGoal):
    openSet = heapdict.heapdict()
    openSet[start] = h(start)
    gScore = {start: 0}

    while len(openSet) > 0:
        _, current = openSet.peekitem()
        if isGoal(current):
            return current
        openSet.pop()

        for neighbor, weight in current.getNeighbors():
            tentativeGScore = gScore[current] + weight
            gScore[neighbor] = tentativeGScore
            openSet[neighbor] = tentativeGScore + h(neighbor)

        del gScore[current]

    return []

class TSPGraph:
    def __init__ (self, n, *args, **kw):
        self.m = np.tile(0, (n, n))

    @staticmethod
    def generateRandom(n):
        graph = TSPGraph(n)

        for row in range(n):
            for col in range(n):
                if row != col:
                    graph.m[row, col] = random.randint(1, 100)

    def getInitialStateNode(self):
        return StateNode(self, (0))

class StateNode:
    def __init__ (self, graph, path, *args, **kw):
        self.path = path
        self.graph = graph

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, item):
        return self.path == item.path
    
    def __ne__(self, item):
        return self.path != item.path

    def __lt__(self, item):
        return True

    def __le__(self, item):
        return True

    def __gt__(self, item):
        return True

    def __ge__(self, item):
        return True

    def getNeighbors(self):
        neighbors = []
        for neighbor_num, weight in enumerate(self.graph.m[self.path[-1], :]):
            if weight > 0:
                neighbors.append((StateNode(self.graph, self.path + (neighbor_num,)), weight))
        return neighbors

    

    