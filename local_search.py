import math
import random
import tsp

def hillClimbing(graph, restarts=1):
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
        segment = path[loc1:loc2]
        rest = path[:loc1] + path[loc2:]
    else:
        segment = path[loc1:] + path[:loc2]
        rest = path[loc2:loc1]

    return (segment, rest)

def simuAnnealing(graph, iterations, cooling_factor):
    path = list(range(graph.n))
    random.shuffle(path)

    for i in range(iterations):
        temp = math.pow(cooling_factor, i)

        seg, rest = get_random_segment(path)
        path_new = []
        if len(seg) == 0 or len(rest) == 0:
            continue
        elif random.randint(0,1) == 0:
            path_new = seg[::-1] + rest
        else:
            loc = random.randint(0, len(rest) - 1)
            path_new = rest[0:loc] + seg + rest[loc:]
        
        if accept_proposal(tsp.path_cost(path, graph), tsp.path_cost(path_new, graph), temp):
            path = path_new

    return path


def cycle_crossover(p1, p2):
    cycle_start = random.randint(0, len(p1) - 1)
    c1 = [None] * len(p1)
    c2 = [None] * len(p2)
    
    i = cycle_start
    while True:
        c1[i] = p1[i]
        c2[i] = p2[i]

        i = p1.index(p2[i])

        if i == cycle_start:
            break

    for i in range(len(p1)):
        if c1[i] == None:
            c1[i] = p2[i]
            c2[i] = p1[i]

    return (c1, c2)

def compute_fitness_and_sort(population, graph):
    a = [None] * len(population)
    for i, path in enumerate(population):
        a[i] = {'cost': tsp.path_cost(path, graph), 'path': path}
    a.sort(key=lambda m: m['cost'])

    return list(map(lambda m: m['path'], a))

def perform_mutation(path):
    seg, rest = get_random_segment(path)
    if random.randint(0,1) == 0:
        return seg[::-1] + rest
    else:
        loc = random.randint(0, len(rest) - 1)
        return rest[0:loc] + seg + rest[loc:]

def genetic(graph, iterations, population_size, mutation_factor):
    if population_size % 2 == 1:
        population_size = population_size + 1

    # generate initial population
    pop = [None] * population_size
    for i in range(population_size):
        pop[i] = list(range(graph.n))
        random.shuffle(pop[i])
    
    # compute fitness
    pop = compute_fitness_and_sort(pop, graph)
    best = pop[0]

    while iterations > 0:
        # do selection
        pop = pop[:len(pop)//2]
        
        #perform crossover
        i = 0
        len_pop = len(pop)
        while i < len_pop:
            c1, c2 = cycle_crossover(pop[i], pop[i + 1])
            pop.append(c1)
            pop.append(c2)
            i = i + 2

        # mutation
        for i in range(len(pop)):
            if random.uniform(0, 1) <= mutation_factor:
                pop[i] = perform_mutation(pop[i])

        # recalculate fitness
        pop = compute_fitness_and_sort(pop, graph)

        if tsp.path_cost(pop[0], graph) > tsp.path_cost(best, graph):
            best = pop[0]

        iterations = iterations - 1

    return best