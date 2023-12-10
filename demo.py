import networkx

# Construct a graph G
G = networkx.DiGraph()
edges_numerical = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (5, 7)]
G.add_edges_from(edges_numerical)
u_index = 0



