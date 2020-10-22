import a_star as a
import local_search as ls
import tsp
import numpy as np

# graph = tsp.TSPGraph.generate_random(5)
graph = tsp.TSPGraph(5)
graph.m = np.array([
    [ 0, 63, 53, 42, 96],
    [63,  0,  8, 98, 97],
    [53,  8,  0, 87, 43],
    [42, 98, 87,  0, 47],
    [96, 97, 43, 47,  0]
])
print(graph.m)
# result = a.a_star(graph.get_start_state_node(), tsp.is_goal, a.h_mst)
print(a.h_smallest_edge(graph.get_start_state_node().get_neighbors()[0][0]))
print(graph.get_start_state_node().get_neighbors()[0][0].path)
# print(result[0].path)