import a_star
import local_search
import tsp

def A_uniformCost():
    graph = tsp.TSPGraph.create_from_file('infile.txt')
    return a_star.a_star(graph.get_start_state_node(), tsp.is_goal, a_star.h_uniform_cost)

def A_randomEdge():
    graph = tsp.TSPGraph.create_from_file('infile.txt')
    return a_star.a_star(graph.get_start_state_node(), tsp.is_goal, a_star.h_random_edge)

def A_cheapestEdge():
    graph = tsp.TSPGraph.create_from_file('infile.txt')
    return a_star.a_star(graph.get_start_state_node(), tsp.is_goal, a_star.h_smallest_edge)

def A_MST():
    graph = tsp.TSPGraph.create_from_file('infile.txt')
    return a_star.a_star(graph.get_start_state_node(), tsp.is_goal, a_star.h_mst)

