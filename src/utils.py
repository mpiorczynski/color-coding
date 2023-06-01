"""Utility functions for the project."""

import pandas as pd
import networkx as nx
from texttable import Texttable
import numpy as np
import matplotlib.pyplot as plt
import random
import argparse
import seaborn as sns

def print_config(num_nodes, num_edges, num_tree_nodes, algorithm, seed):
    """
    Function to print the logs in a nice tabular format.
    :param args: Parameters used for the model.
    """
    t = Texttable()
    t.add_rows([["Parameter", "Value"],
                ["Graph type", "Erdos-Renyi"],
                ["Number of vertices in the graph", num_nodes],
                ["Number of edges in the graph", num_edges],
                ["Number of vertices in the tree", num_tree_nodes],
                ["Algorithm", algorithm],
                ["Random seed", seed],
    ])
    print(t.draw())

def read_graph(path):
    """
    Function to read the graph from the path.
    :param path: Path to the edge list.
    :return graph: NetworkX object returned.
    """
    graph = nx.read_edgelist(path, delimiter=",", nodetype=int)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    return graph


def save_graph(graph, path):
    """
    Function to save a graph in a edgelist format.
    :param graph: Graph to save.
    :param path: Path where save.
    """
    nx.write_edgelist(graph, path, delimiter=",", data=False)

def parse_args():
    parser = argparse.ArgumentParser(description="Run isomorphic subtree search.")
    parser.add_argument("-n", type=int, default=100, help="Number of vertices in the graph.")
    parser.add_argument("-k", type=int, default=5, help="Number of vertices in the tree.")
    parser.add_argument("--seed", type=int, default=123, help="Random seed.")
    parser.add_argument("--algorithm", type=str, default="color_coding", choices=["brute_force", "color_coding"], help="Algorithm to implementation run.")

    args = parser.parse_args()
    return args

def set_seed(seed):
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


def plot_degree_distribution(graph):
    degrees = [graph.degree(n) for n in graph.nodes]
    sns.histplot(degrees, binwidth=1)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution')
    plt.show()

def network_summary(network):
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