"""Utility functions for the project."""

import argparse
import os
import random
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from texttable import Texttable


def print_config(graph_path, num_nodes, num_edges, num_tree_nodes, algorithm, seed):
    """Print logs in a nice tabular format."""
    t = Texttable()
    t.add_rows([["Parameter", "Value"],
                ["Graph path", graph_path],
                ["Number of vertices in the graph", num_nodes],
                ["Number of edges in the graph", num_edges],
                ["Number of vertices in the tree", num_tree_nodes],
                ["Algorithm", algorithm],
                ["Random seed", seed],
    ])
    print(t.draw())

def read_graph(path: str) -> nx.Graph:
    """Read graph in a edgelist format."""
    graph = nx.read_edgelist(path, delimiter=",", nodetype=int)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    return graph

def save_graph(graph: nx.Graph, path: str):
    """Save graph in a edgelist format."""
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    graph = add_selfloops_for_isolated(graph)
    nx.write_edgelist(graph, path, delimiter=",", data=False)

def add_selfloops_for_isolated(graph: nx.Graph):
    """Utility function to add self loops to a graph to save isolated nodes in edgelist format."""
    isolated_nodes = [node for node in graph.nodes if graph.degree(node) == 0]
    for node in isolated_nodes:
        graph.add_edge(node, node)

    return graph

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run isomorphic subtree search.")
    parser.add_argument("--graph_path", type=str, default="data/erdos_renyi/erdos_renyi_100_0.1_123.edgelist", help="Input graph path.")
    parser.add_argument("--num_tree_nodes", type=int, default=5, help="Number of nodes in the tree.")
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    parser.add_argument("--algorithm", type=str, default="color_coding", choices=["brute_force", "color_coding"], help="Algorithm to implementation run.")

    args = parser.parse_args()
    return args

def set_seed(seed: int):
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)

def plot_graph_tree(graph, tree):
    """Plot graph and tree."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    ax1.set_title("Graph")
    ax2.set_title("Tree")
    nx.draw(graph, with_labels=False, width=0.1, node_size=10, ax=ax1)
    nx.draw(tree, with_labels=False, width=0.1, node_size=10, ax=ax2)
    fig.savefig("graph_tree.png")


def plot_degree_distribution(graph: nx.Graph):
    """Plot degree distribution of a graph."""
    degrees = [graph.degree(n) for n in graph.nodes]
    sns.histplot(degrees, binwidth=1)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution')
    plt.show()

def network_summary(network: nx.Graph):
    """Calculate summary statistics for a network."""
    summary = {}

    summary['num_nodes'] = nx.number_of_nodes(network)
    summary['num_edges'] = nx.number_of_edges(network)
    if nx.is_connected(network):
        summary['avg_shortest_path_length'] = nx.average_shortest_path_length(network)
        summary['diameter'] = nx.diameter(network)
    summary['transitivity'] = nx.transitivity(network)
    summary['clustering_coefficient'] = nx.average_clustering(network)
    summary['density'] = nx.density(network)
    summary['avg_degree'] = np.array([d for n, d in network.degree()]).sum()/ nx.number_of_nodes(network)
    summary['num_connected_components'] = nx.number_connected_components(network)
    return summary