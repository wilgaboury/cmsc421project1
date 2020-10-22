import heapdict
import numpy as np
import random
import tsp

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
    n = node.graph.n
    rows = list(set(range(n)) - set(node.path))
    for row in rows:
        result = result + min(filter(lambda x: x > 0, node.graph.m[row,:]))
    return result

def h_mst(node):
    n = node.graph.m.shape[0]
    m = node.graph.m

    result = 0

    f = set(node.path[0:-1])
    c = heapdict.heapdict()
    c[node.path[-1]] = 0

    prev = [None] * node.graph.n
    if len(node.path) > 1:
        prev[node.path[-1]] = node.path[-1]
    else:
        prev[0] = 0

    while len(c) > 0:
        v, _ = c.popitem()
        f = f | {v}
        result = result + m[v, prev[v]]
        neighbors = set(range(n)) - f
        for neighbor in neighbors:
            if (not neighbor in c) or m[v, neighbor] < c[neighbor]:
                c[neighbor] = m[v, neighbor]
                prev[neighbor] = v

    return result  

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