#!/usr/bin/env python3
import shutil
import os
from argparse import ArgumentParser
import networkx
import numpy as np


def parse_args():
    parser = ArgumentParser(description="Noir prover script")
    parser.add_argument("--prover_toml_name", type=str, help="prover toml name")
    parser.add_argument("--proof_output", type=str, help="proof output file")
    return parser.parse_args()


def setup_circuit(
    graph, 
    u_index,
    prover_toml_name,
):  
    # Process the graph 
    n_nodes = len(graph.nodes())
    NUM_NODES = 10
    if n_nodes > NUM_NODES:
        raise ValueError(f"The number of nodes in the graph exceeds the maximum limit of {NUM_NODES}.")

    # Write to prover toml
    prover_toml_path = f"{prover_toml_name}.toml"
    with open(prover_toml_path, "w") as f:

        circuit_input = ""
        # Go through all the real nodes here
        for i in range(n_nodes):
            adj_list = [True if graph.has_edge(i, j) else False for j in range(n_nodes)] \
                + [False for j in range(NUM_NODES-n_nodes)]
            adj_list = str(adj_list).lower()
            
            edge_matrix = [0 for j in range(n_nodes)] \
                + [0 for j in range(NUM_NODES-n_nodes)]
            node_text = f"""[[graph.nodes]]
index = {i}
value = {0}
adj_list = {adj_list}
edge_matrix = {edge_matrix}

"""
            circuit_input += node_text
        
        # Add padding
        for i in range(NUM_NODES-n_nodes):
            adj_list = [False for j in range(NUM_NODES)]
            adj_list = str(adj_list).lower()
            edge_matrix = [0 for j in range(NUM_NODES)]
            node_text = f"""[[graph.nodes]]
index = {i+n_nodes}
value = {0}
adj_list = {adj_list}
edge_matrix = {edge_matrix}

"""
            circuit_input += node_text

        adj_list = [True if graph.has_edge(u_index, j) else False for j in range(n_nodes)] \
                + [False for j in range(NUM_NODES-n_nodes)]
        adj_list = str(adj_list).lower()
        edge_matrix = [0 for j in range(n_nodes)]\
                + [0 for j in range(NUM_NODES-n_nodes)]
        circuit_input += f"""[u]
index = {u_index}
value = {0}
adj_list = {adj_list}
edge_matrix = {edge_matrix}
"""

        f.write(circuit_input)


def solve_circuit(prover_toml_name, proof_output):
    import subprocess

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

    # shutil.copyfile(os.path.join("proofs", f"{prover_toml_name}.proof"), proof_output)


def verify_circuit(proof_output):
    import subprocess
    subprocess.check_call(
        [
            "nargo",
            "verify",
            "-v",
            proof_output,
        ]
    )

def work(graph, u_index, prover_toml_name, proof_output):
    print("Setting up circuit...")
    setup_circuit(
        graph, u_index, prover_toml_name
    )

    print("Proving circuit...")
    solve_circuit(prover_toml_name, proof_output)
        
    print("Verifying circuit...")
    verify_circuit(proof_output)

    print("Done!")


def main(args=None):
    if args is None:
        args = parse_args()

    # Construct a graph G
    G = networkx.DiGraph()
    edges_numerical = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (5, 7)]
    G.add_edges_from(edges_numerical)
    u_index = 0


    work(
        G,
        u_index,
        args.prover_toml_name,
        args.proof_output,
    )


if __name__ == "__main__":
    main()