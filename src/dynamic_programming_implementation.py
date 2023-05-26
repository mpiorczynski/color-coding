"""Implementation of color coding for finding a subtree with k vertices in a graph using dynamic programming."""
from re import sub
import networkx as nx
import math
import random
import numpy as np
import itertools
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import argparse
from texttable import Texttable
from traitlets import default
from collections import defaultdict

def generate_k_vertex_subtrees(tree, root, k, visited=None):
    """Generate all k-vertices rooted subtrees of a tree with DFS with limited by k depth."""
    if k == 1:
        subtree = nx.Graph()
        subtree.add_node(root)
        yield subtree
    else:
        for node in tree.neighbors(root):
            if node is not visited:
                visited = node
                for subtree in generate_k_vertex_subtrees(tree, node, k-1, visited=visited):
                    subtree.add_edge(root, node)
                    # if len(subtree.nodes) == k:
                    #     yield subtree
                    yield subtree


def color_coding(graph, tree):
    n = len(graph.nodes)
    k = len(tree.nodes)

    # random coloring
    for v in graph.nodes:
        graph.nodes[v]['color'] = random.choice(range(k))

    memory = defaultdict(list)
    for c in range(k):
        for root in range(k):
            for subtree in generate_k_vertex_subtrees(tree, root, 1):
                for node in range(n):
                    key = (node, subtree, root)
                    if graph.nodes[node]['color'] == c:
                        memory[key].append({c})
    
    for i in range(2, k+1):
        for colors in itertools.combinations(range(k), i):
            for root in range(k):
                for subtree in generate_k_vertex_subtrees(tree, root, i):
                    for node in range(n):
                        for node_neighbor in graph.neighbors(node):
                            key = (node, subtree2, root)
                            subtree2 = subtree.copy()
                            subtree2.add_node(node_neighbor)
                            if colors.isdisjoint(memory[(node_neighbor, subtree2, root)]):
                                memory[key].append(colors)

    print(memory)
    return False



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Color Coding.")
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
                ["Number of repeats.", math.ceil(math.exp(args.k))]
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

    # run color coding
    flag = color_coding(graph, tree)
    print(f"Is there a subtree with {args.k} vertices in the graph?: {flag}")