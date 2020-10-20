import math
import random
import tsp

def hill_climb(graph, restarts=1):
    result = list(range(graph.n))
    while restarts > 0:
        path = list(range(graph.n))
        random.shuffle(path)

        while True:
            new_path = path.copy()
            best_path = new_path.copy()
            best_cost = tsp.path_cost(best_path, graph)

            for i in range(-1, graph.n - 1):
                new_path[i], new_path[i + 1] = new_path[i + 1], new_path[i]
                new_cost = tsp.path_cost(new_path, graph)
                if new_cost < best_cost:
                    best_path = new_cost
                    best_path = new_path.copy()
                new_path[i], new_path[i + 1] = new_path[i + 1], new_path[i]
            

            if best_cost == tsp.path_cost(path, graph):
                break
            
            path = best_path

        if tsp.path_cost(path, graph) < tsp.path_cost(result, graph):
            result = path

        restarts = restarts - 1

    return result

def accept_proposal(current, proposal, temp):
    if proposal < current:
        return True
    if temp == 0:
        return False

    prob = math.exp(-(proposal - current) / temp)
    return random.uniform(0, 1) < prob

def get_random_segment(path):
    loc1 = random.randint(0, len(path) - 1)
    loc2 = random.randint(0, len(path) - 2)
    if loc2 >= loc1:
        loc2 = loc2 + 1

    rest = []
    segment = []

    if loc1 < loc2:
        segment = path[loc1:loc2+1]
        rest = path[0:loc1] + path[loc2+1:len(path)]
    else:
        segment = path[loc1:len(path)] + path[0:loc2]
        rest = path[loc2+1:loc1]

    return (segment, rest)

def simulated_annealing(graph, iterations):
    path = list(range(graph.n))
    random.shuffle(path)

    for i in range(iterations):
        temp = math.pow(0.95, i)

        seg, rest = get_random_segment(path)
        path_new = []
        if len(seg) == 0 or len(rest) == 0:
            continue
        elif random.randint(0,1) == 0:
            path_new = seg[::-1] + rest
        else:
            loc = random.randint(0, len(rest) - 1)
            path_new = rest[0:loc] + seg + rest[loc:len(rest)]
        
        if accept_proposal(tsp.path_cost(path, graph), tsp.path_cost(path_new, graph), temp):
            path = path_new

    return path

