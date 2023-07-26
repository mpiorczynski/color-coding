"""Finding an isomorphic subtree with k vertices in a graph with n vertices using a brute force."""
import networkx as nx
import math
import numpy as np
import itertools
from tqdm.auto import tqdm

def find_isomorphic_subtree(graph: nx.Graph, tree: nx.Graph) -> bool:
    """Find an isomorphic subtree in a graph using brute force."""
    nodes = list(graph.nodes)
    num_tree_nodes = len(tree.nodes)
    num_nodes = len(graph.nodes)
    tree_adj = nx.adjacency_matrix(tree).todense()

    # Generate all possible combinations of nodes for subgraph of input size
    for combination in tqdm(itertools.combinations(nodes, num_tree_nodes), desc="Looking for an isomorphic subtree.", total=math.comb(num_nodes, num_tree_nodes)):
        subgraph_adj = nx.adjacency_matrix(graph, combination).todense()
        if np.sum(subgraph_adj) / 2 < num_tree_nodes - 1:
            continue
        else:
            for p in itertools.permutations(range(num_tree_nodes)):
                if np.all(subgraph_adj[p, :][:, p] - tree_adj >= 0):
                    return True

    return False