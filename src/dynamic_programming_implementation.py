"""Implementation of color coding for finding a subtree with k vertices in a graph using dynamic programming."""
import networkx as nx
import math
import random
import numpy as np
import itertools
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import argparse
from texttable import Texttable


def find_colors(graph, node, tree, root, memory):
    # print(f"Tree root: {root}")
    # print(f"Tree nodes: {tree.nodes}")

    if len(tree.nodes) == 1:
        return [{graph.nodes[node]['color']}]
    else:
        colors = []
        tree_without_edge = tree.copy()

        root_neighbour = random.choice(list(tree.neighbors(root)))
        # print(f"Splitting at: ({root}, {root_neighbour})")
        tree_without_edge.remove_edge(root, root_neighbour)

        connected_components = [tree_without_edge.subgraph(c) for c in nx.connected_components(tree_without_edge)]  # components sorted by size
        subtree1, subtree2 = connected_components[:2]
        if root_neighbour in subtree1.nodes:
            subtree1, subtree2 = subtree2, subtree1
        
        subtree1_key = (node, tuple(subtree1.nodes), root)
        if subtree1_key not in memory:
            memory[subtree1_key] = find_colors(graph, node, subtree1, root, memory)
        
        colors1 = memory[subtree1_key]

        # print(colors1)
        for node_neighbor in graph.neighbors(node):
            subtree2_key = (node_neighbor, tuple(subtree2.nodes), root_neighbour)
            if subtree2_key not in memory:
                memory[subtree2_key] = find_colors(graph, node_neighbor, subtree2, root_neighbour, memory)
            
            colors2 = memory[subtree2_key]
            
            for c1, c2 in itertools.product(colors1, colors2):
                if c1.isdisjoint(c2):
                    colors.append(set.union(c1, c2))
        
        return colors


def color_coding(graph, tree):
    num_tree_nodes = len(tree.nodes)
    num_nodes = len(graph.nodes)

    num_repeats = math.ceil(math.exp(num_tree_nodes))
    root_choices = list(range(num_tree_nodes))
    # num_repeats = 100
    
    for _ in tqdm(range(num_repeats)):
        # random coloring
        for v in graph.nodes:
            graph.nodes[v]['color'] = random.choice(root_choices)

        root = random.choice(root_choices)
        memory = {}
        for node in range(num_nodes):
            colors = find_colors(graph, node, tree, root, memory)
            if colors:
                return True
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