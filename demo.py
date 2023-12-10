from graphite.setup_custom import bfs
import networkx
import pickle

# Construct a graph G
G = networkx.DiGraph()

with open("graph.gpickle", "rb") as f:
        G = pickle.load(f)

bfs(G, 0)
