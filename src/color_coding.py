"""Implementation of color coding for finding an isomorphic subtree with k vertices in a graph with n vertices using dynamic programming."""
import networkx as nx
import math
import random
import itertools
from tqdm.auto import tqdm
from utils import *

def color_graph(graph, colors):
    """
    Function randomly colors graph using given colors.
    :param graph: graph to color
    :param colors: colors to use
    :return: colored graph
    """
    for v in graph.nodes:
        graph.nodes[v]['color'] = random.choice(colors)
    return graph

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

        subtree1, subtree2 = (tree_without_edge.subgraph(c) for c in nx.connected_components(tree_without_edge))  # components sorted by size
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


def find_isomorphic_subtree(graph, tree):
    """
    Function solves tree subgraph isomorphism problem.
    :param graph: graph in which we are looking for an isomorphic subtree
    :param tree: tree isomorphic to the subtree we are looking for
    :return: True or False
    """
    num_tree_nodes = len(tree.nodes)
    num_nodes = len(graph.nodes)

    # num_repeats = math.ceil(math.exp(num_tree_nodes))
    num_repeats = 100
    
    for _ in tqdm(range(num_repeats), desc="Looking for an isomorphic subtree."):
        graph = color_graph(graph, range(num_tree_nodes))

        root = random.choice(range(num_tree_nodes))
        memory = {}
        for node in range(num_nodes):
            colors = find_colors(graph, node, tree, root, memory)
            if colors:
                return True

    return False