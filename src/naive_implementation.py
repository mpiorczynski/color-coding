"""Naive implementation of color coding for finding a subtree with k vertices in a graph using recursion."""
import networkx as nx
import math
import random
import numpy as np
import itertools
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

seed = 123
n = 100
k = 5

random.seed(seed)
np.random.seed(seed)

def find_colors(graph, node, tree, root):
    # print(f"Tree root: {root}")
    # print(f"Tree nodes: {tree.nodes}")

    if len(tree.nodes) == 1:
        return([{graph.nodes[node]['color']}])
    else:
        colors = []
        tree = tree.copy()

        root_neighbour = random.choice(list(tree.neighbors(root)))
        # print(f"Splitting at: ({root}, {root_neighbour})")
        tree.remove_edge(root, root_neighbour)

        subtree1, subtree2 = (tree.subgraph(c).copy() for c in nx.connected_components(tree))  # components sorted by size
        if root_neighbour in subtree1.nodes:
            subtree1, subtree2 = subtree2, subtree1

        colors1 = find_colors(graph, node, subtree1, root)
        # print(colors1)
        for node_neighbor in graph.neighbors(node):
            colors2 = find_colors(graph, node_neighbor, subtree2, root_neighbour)

            for c1, c2 in itertools.product(colors1, colors2):
                if c1.isdisjoint(c2):
                    colors.append(set.union(c1, c2))
        
        return colors


def color_coding(graph, tree):
    k = len(tree.nodes)

    num_repeats = math.ceil(math.exp(k))
    # num_repeats = 100
    print("Number of repeats: ", num_repeats)

    for _ in tqdm(range(num_repeats)):
        # random coloring
        for v in graph.nodes:
            graph.nodes[v]['color'] = random.choice(range(k))

        root = random.choice(range(k))
        for node in range(len(graph.nodes)):
            colors = find_colors(graph, node, tree, root)
            if colors:
                return True

    return False



if __name__ == "__main__":

    # generate random graph using erdos renyi model
    graph = nx.erdos_renyi_graph(n, p=0.1, seed=seed)

    fig = plt.figure()
    nx.draw(graph, with_labels=False, width=0.1, node_size=10, ax=fig.add_subplot())
    fig.savefig("graph.png")

    # generate random tree
    tree = nx.random_tree(k, seed=seed)

    fig = plt.figure()
    nx.draw(tree, with_labels=True, node_size=10, ax=fig.add_subplot())
    fig.savefig("tree.png")

    # run color coding
    flag = color_coding(graph, tree)
    print(f"Is there a subtree with {k} vertices in the graph?: {flag}")