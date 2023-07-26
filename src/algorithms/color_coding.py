"""Implementation of color coding for finding an isomorphic subtree with k vertices in a graph with n vertices using dynamic programming."""
import networkx as nx
import math
import random
import itertools
from tqdm.auto import tqdm
from src.algorithms.tree import Tree
    
def color_graph(graph: nx.Graph, colors: int):
    """Randomly color graph nodes with colors in range 0 to k-1."""
    for v in graph.nodes:
        graph.nodes[v]['color'] = random.choice(colors)
    return graph

def find_colors(graph, node, tree, memory):
    if len(tree.nodes) == 1:
        return [{graph.nodes[node]['color']}]
    else:
        colors = []
        subtree1, subtree2 = tree.random_split()
        
        subtree1_key = (node, tuple(subtree1.nodes), subtree1.root)
        if subtree1_key not in memory:
            memory[subtree1_key] = find_colors(graph, node, subtree1, memory)
        
        colors1 = memory[subtree1_key]

        for node_neighbor in graph.neighbors(node):
            subtree2_key = (node_neighbor, tuple(subtree2.nodes),  subtree2.root)
            if subtree2_key not in memory:
                memory[subtree2_key] = find_colors(graph, node_neighbor, subtree2, memory)
            
            colors2 = memory[subtree2_key]
            
            for c1, c2 in itertools.product(colors1, colors2):
                if c1.isdisjoint(c2):
                    colors.append(set.union(c1, c2))
        
        return colors


def find_isomorphic_subtree(graph: nx.Graph, tree: nx.Graph) -> bool:
    """Find an isomorphic subtree in a graph using color coding."""
    # Parse from NetworkX object to custom object for efficient constant time splitting
    tree = Tree.from_networkx(tree)

    num_nodes = graph.number_of_nodes()
    num_tree_nodes = tree.number_of_nodes()

    # numbe of repeats for constant error probability
    num_repeats = math.ceil(math.exp(num_tree_nodes))
    
    for _ in tqdm(range(num_repeats), desc="Looking for an isomorphic subtree."):
        graph = color_graph(graph, range(num_tree_nodes))

        memory = {}
        for node in range(num_nodes):
            colors = find_colors(graph, node, tree, memory)
            if colors:
                return True

    return False