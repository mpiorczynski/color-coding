"""Naive implementation of color coding for finding a subtree with k vertices in a graph using recursion."""
import networkx as nx
import math
import random
import numpy as np

seed = 123
n = 10
k = 5

random.seed(seed)
np.random.seed(seed)

def find_colors(graph, node, tree, root):
    # print(f"Tree root: {root}")
    # print(f"Tree nodes: {tree.nodes}")

    if len(tree.nodes) == 1:
        return({graph.nodes[node]['color']})
    else:
        colors = set()
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
            if colors1.isdisjoint(colors2):
                colors = colors.union(colors1).union(colors2)
        return(colors)


def color_coding(graph, tree):
    root = random.choice(range(len(tree.nodes)))
    for node in range(len(graph.nodes)):
        colors = find_colors(graph, node, tree, root)
        if colors:
            return True

    return False



if __name__ == "__main__":
    # generate random graph using erdos renyi model
    graph = nx.erdos_renyi_graph(n, p=0.1, seed=seed) 

    # color its nodes
    for v in graph.nodes:
        graph.nodes[v]['color'] = random.choice(range(k))

    # generate random tree
    tree = nx.random_tree(k, seed=seed)

    # run color coding
    color_coding(graph, tree)