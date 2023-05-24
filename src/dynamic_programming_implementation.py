"""Implementation of color coding for finding a subtree with k vertices in a graph using dynamic programming."""
import networkx as nx
import math
import random
import numpy as np
import matplotlib.pyplot as plt

seed = 123
n = 10
k = 10

random.seed(seed)
np.random.seed(seed)

def find_colors(graph, node, tree, root, memory):
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
        
        subtree1_key = (node, subtree1, root)
        if subtree1_key not in memory:
            colors1 = find_colors(graph, node, subtree1, root, memory)
            memory[subtree1_key] = colors1

        # print(colors1)
        for node_neighbor in graph.neighbors(node):
            subtree2_key = (node_neighbor, subtree2, root_neighbour)
            if subtree2_key not in memory:
                colors2 = find_colors(graph, node_neighbor, subtree2, root_neighbour, memory)
                memory[subtree2_key] = colors2
            
            if colors1.isdisjoint(colors2):
                colors = colors.union(colors1).union(colors2)
        
        return colors


def color_coding(graph, tree):
    k = len(tree.nodes)
    for _ in range(math.ceil(math.exp(k))):
        # random coloring
        for v in graph.nodes:
            graph.nodes[v]['color'] = random.choice(range(k))

        root = random.choice(range(k))
        memory = {}
        for node in range(len(graph.nodes)):
            colors = find_colors(graph, node, tree, root, memory)
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