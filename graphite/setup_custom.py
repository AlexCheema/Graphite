#!/usr/bin/env python3
import shutil
import json
import os
from argparse import ArgumentParser
import networkx
import numpy as np
import pickle
from typing import List

NUM_NODES = 10

def parse_args():
    parser = ArgumentParser(description="Noir prover script")
    parser.add_argument("--algorithm", type=str, help="algorithm name")
    parser.add_argument("--prover_toml_name", type=str, help="prover toml name")
    parser.add_argument("--proof_output", type=str, help="proof output file")
    return parser.parse_args()


def check_graph(graph):
    # Process the graph 
    n_nodes = len(graph.nodes())
    if n_nodes > NUM_NODES:
        raise ValueError(f"The number of nodes in the graph exceeds the maximum limit of {NUM_NODES}.")


    def check_edge_weights(graph):
        for u, v, data in graph.edges(data=True):
            if not isinstance(data.get('weight', 1), int):
                raise ValueError(f"Edge weight between nodes {u} and {v} is not an integer.")

    check_edge_weights(graph)

def setup_circuit(
    graph, 
    u_index,
    prover_toml_name,
    algorithm,
):  
    # Process the graph 
    n_nodes = len(graph.nodes())

    # Write to prover toml
    prover_toml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{algorithm}/{prover_toml_name}.toml")
    with open(prover_toml_path, "w") as f:

        circuit_input = ""
        public_inputs = []
        # Go through all the real nodes here
        for i in range(n_nodes):
            adj_list = [True if graph.has_edge(i, j) else False for j in range(n_nodes)] \
                + [False for j in range(NUM_NODES-n_nodes)]
            adj_list_s = str(adj_list).lower()
            
            edge_matrix = [graph.get_edge_data(i, j)['weight'] if graph.has_edge(i, j) else 0 for j in range(n_nodes)] \
                + [0 for j in range(NUM_NODES-n_nodes)]
            node_text = f"""[[graph.nodes]]
index = {i}
value = {0}
adj_list = {adj_list_s}
edge_matrix = {edge_matrix}

"""
            circuit_input += node_text
            public_inputs += [i, 0, *adj_list, *edge_matrix]
        
        # Add padding
        for i in range(NUM_NODES-n_nodes):
            adj_list = [False for j in range(NUM_NODES)]
            adj_list_s = str(adj_list).lower()
            edge_matrix = [0 for j in range(NUM_NODES)]
            node_text = f"""[[graph.nodes]]
index = {i+n_nodes}
value = {0}
adj_list = {adj_list_s}
edge_matrix = {edge_matrix}

"""
            circuit_input += node_text
            public_inputs += [i+n_nodes, 0, *adj_list, *edge_matrix]

        adj_list = [True if graph.has_edge(u_index, j) else False for j in range(n_nodes)] \
                + [False for j in range(NUM_NODES-n_nodes)]
        adj_list_s = str(adj_list).lower()
        edge_matrix = [graph.get_edge_data(u_index, j)['weight'] if graph.has_edge(u_index, j) else 0 for j in range(n_nodes)]\
                + [0 for j in range(NUM_NODES-n_nodes)]
        circuit_input += f"""[u]
index = {u_index}
value = {0}
adj_list = {adj_list_s}
edge_matrix = {edge_matrix}
"""
        public_inputs += [u_index, 0, *adj_list, *edge_matrix]

        f.write(circuit_input)
        print(json.dumps(public_inputs))


def solve_circuit(prover_toml_name, proof_output, algorithm):
    import subprocess

    os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), algorithm))
    subprocess.check_output(
        [
            "nargo",
            "prove",
            "-p",
            prover_toml_name,
            "-v",
            proof_output,
        ]
    )
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # shutil.copyfile(os.path.join("proofs", f"{prover_toml_name}.proof"), proof_output)


def verify_circuit(proof_output, algorithm):
    import subprocess

    os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), algorithm))
    subprocess.check_call(
        [
            "nargo",
            "verify",
            "-v",
            proof_output,
        ]
    )
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

def work(graph, u_index, prover_toml_name, proof_output, algorithm):
    print("Checking graph...")
    check_graph(graph)

    print("Setting up circuit...")
    setup_circuit(
        graph, u_index, prover_toml_name, algorithm
    )

    print("Proving circuit...")
    solve_circuit(prover_toml_name, proof_output, algorithm)

    print("Verifying circuit...")
    verify_circuit(proof_output, algorithm)

    print("Done!")

def no_cycle(G,
        u_index,
        prover_toml_name="tryprover",
        proof_output="tryoutput"):
    work(
        G,
        u_index,
        prover_toml_name,
        proof_output,
        "no_cycle"
    )
    return "", ""

def bfs(G,
        u_index,
        prover_toml_name="tryprover",
        proof_output="tryoutput") -> List[int]:
    work(
        G,
        u_index,
        prover_toml_name,
        proof_output,
        "bfs"
    )
    return "", ""


def main(args=None):
    if args is None:
        args = parse_args()

    # Construct a graph G
    G = networkx.DiGraph()
    edges_numerical = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (5, 7)]
    G.add_edges_from(edges_numerical)
    u_index = 0

    # Save a static file of the graph G
    # with open("graph.gpickle", "wb") as f:
    #     pickle.dump(G, f)

    # Load a static file of the graph G
    with open("graph.gpickle", "rb") as f:
        G = pickle.load(f)

    work(
        G,
        u_index,
        args.prover_toml_name,
        args.proof_output,
        args.algorithm,
    )


if __name__ == "__main__":
    main()