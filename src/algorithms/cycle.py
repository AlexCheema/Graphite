import networkx as nx
def detect_cycles(graph):
    """
    Detect cycles in a graph.
    
    :param graph: NetworkX graph
    :return: List of cycles, where each cycle is a list of nodes
    """
    cycles = list(nx.simple_cycles(graph))
    return cycles

# Example usage
if __name__ == "__main__":
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges to the graph
    # Example: G.add_edge('A', 'B') indicates a link from 'A' to 'B'

    # Detect cycles
    cycles = detect_cycles(G)

    # Display cycles
    print("Cycles:", cycles)

