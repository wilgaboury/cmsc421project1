import numpy as np
import random

class TSPGraph:
    def __init__ (self, n, *args, **kw):
        self.n = n
        self.m = np.tile(0, (n, n))

    def get_start_state_node(self):
        return StateNode(self, (0,))

    def write_to_file(self, file_name):
        f = open(file_name, 'w')
        f.write(str(self.n) + '\n')
        for row in range(self.n):
            f.write(', '.join(map(lambda e: str(e), self.m[row,:])) + '\n')

    @staticmethod
    def generate_random(n):
        graph = TSPGraph(n)
        for row in range(n - 1):
            for col in range(row + 1, n):
                value = random.randint(1, 100)
                graph.m[row, col] = value
                graph.m[col, row] = value
        return graph

    @staticmethod
    def create_from_file(file_name):
        f = open(file_name, 'r')
        graph = TSPGraph(int(f.readline()))
        for row in range(graph.n):
            for col, elem in enumerate(f.readline().split(', ')):
                graph.m[row, col] = int(elem)
        return graph

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
            if weight > 0 and (not neighbor_num in self.path or (len(self.path) == self.graph.n and neighbor_num == 0)):
                neighbors.append((StateNode(self.graph, self.path + (neighbor_num,)), weight))
        return neighbors
    
    def cost(self):
        shortened_path = self.path[:len(self.path)-1]
        return path_cost(shortened_path, self.graph)



def is_goal(node):
    n = node.graph.m.shape[0]
    return node.path[0] == 0 and node.path[-1] == 0 and len(node.path) == n + 1

def path_cost(path, graph):
    result = 0
    for i in range(len(path) - 1):
        result = result + graph.m[path[i], path[i + 1]]
    return result + graph.m[path[0], path[-1]]