"""Finding a subtree with k vertices in a graph using a brute force."""
import networkx as nx
import math
import random
import numpy as np
import itertools
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
from texttable import Texttable


def find_isomorphic_subtree(graph, tree):
    """
    Function solves tree subgraph isomorphism problem (brute force approach).
    :param graph: graph in which we are looking for an isomorphic subtree
    :param tree: tree isomorphic to the subtree we are looking for
    :return: True or False
    """
    nodes = list(graph.nodes)
    k = len(tree.nodes)

    # Generate all possible combinations of nodes for subgraph of input size
    for combination in tqdm(itertools.combinations(nodes, k), desc="Looking for isomorphic subtree"):
        subgraph = graph.subgraph(combination)
        if nx.is_isomorphic(subgraph, tree):
            return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run brute force.")
    parser.add_argument("-n", type=int, default=100, help="Number of vertices in the graph.")
    parser.add_argument("-k", type=int, default=5, help="Number of vertices in the tree.")
    parser.add_argument("--seed", type=int, default=123, help="Random seed.")

    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    t = Texttable()
    t.add_rows([["Parameter", "Value"],
                ["Number of vertices in the graph.", args.n],
                ["Number of vertices in the tree.", args.k],
                ["Random seed.", args.seed],
    ])
    print(t.draw())

    # generate random graph using erdos renyi model
    graph = nx.erdos_renyi_graph(args.n, p=0.1, seed=args.seed)
    
    # generate random tree
    tree = nx.random_tree(args.k, seed=args.seed)

    # plot graph and tree
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    ax1.set_title("Graph")
    ax2.set_title("Tree")
    nx.draw(graph, with_labels=False, width=0.1, node_size=10, ax=ax1)
    nx.draw(tree, with_labels=False, width=0.1, node_size=10, ax=ax2)
    fig.savefig("graph_tree.png")

    # run brute force
    flag = find_isomorphic_subtree(graph, tree)
    print(f"Is there a isomorphic subtree with {args.k} vertices in the graph?: {flag}")
