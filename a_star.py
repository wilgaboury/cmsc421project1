import heapdict
import numpy as np
import random

def h_uniform_cost(_):
    return 0

def h_random_edge(node):
    result = 0
    n = node.graph.m.shape[0]
    rows = list(set(range(n)) - set(node.path))
    for row in rows:
        i = random.randint(0, n - 2)
        if i > row:
            i = i + 1
        result = result + node.graph.m[row, i]
    return result

def h_smallest_edge(node):
    result = 0
    n = node.graph.m.shape[0]
    rows = list(set(range(n)) - set(node.path))
    for row in rows:
        result = result + min(filter(lambda x: x > 0, node.graph.m[row, :]))
    return result

def is_goal(node):
    n = node.graph.m.shape[0]
    return node.path[0] == 0 and node.path[-1] == 0 and len(node.path) == n + 1

# Reference implementation of A*

# def reconstruct_path(cameFrom, current):
#     totalPath = [current]
#     while current in cameFrom:
#         current = cameFrom[current]
#         totalPath.append(current)
#     return totalPath

# def a_star(start, h, isGoal):
#     openSet = heapdict.heapdict()
#     openSet[start] = h(start)
#     cameFrom = {}
#     gScore = {start: 0}

#     while len(openSet) > 0:
#         _, current = openSet.peekitem()
#         if isGoal(current):
#             return reconstruct_path(cameFrom, current)
#         openSet.pop()

#         for neighbor, weight in current.getNeighbors():
#             tentativeGScore = gScore[current] + weight
#             if (not (neighbor in gScore)) or tentativeGScore < gScore[neighbor]:
#                 cameFrom[neighbor] = current
#                 gScore[neighbor] = tentativeGScore
#                 openSet[neighbor] = tentativeGScore + h(neighbor)

#     return []

# efficent version of A* for that basically only works for this problem
def a_star(start, isGoal, h):
    nodes_processed = 0

    openSet = heapdict.heapdict()
    openSet[start] = h(start)
    gScore = {start: 0}

    while len(openSet) > 0:
        nodes_processed = nodes_processed + 1

        current, _ = openSet.peekitem()
        if isGoal(current):
            return (current, nodes_processed)
        openSet.popitem()

        for neighbor, weight in current.get_neighbors():
            tentativeGScore = gScore[current] + weight
            gScore[neighbor] = tentativeGScore
            openSet[neighbor] = tentativeGScore + h(neighbor)

        del gScore[current]

    return []

class TSPGraph:
    def __init__ (self, n, *args, **kw):
        self.m = np.tile(0, (n, n))

    @staticmethod
    def generate_random(n):
        graph = TSPGraph(n)
        for row in range(n - 1):
            for col in range(row + 1, n):
                value = random.randint(1, 100)
                graph.m[row, col] = value
                graph.m[col, row] = value
        return graph

    def get_start_state_node(self):
        return StateNode(self, (0,))

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

    def get_neighbors(self):
        neighbors = []
        for neighbor_num, weight in enumerate(self.graph.m[self.path[-1], :]):
            if weight > 0 and (neighbor_num == 0 or not neighbor_num in self.path):
                neighbors.append((StateNode(self.graph, self.path + (neighbor_num,)), weight))
        return neighbors

    

    