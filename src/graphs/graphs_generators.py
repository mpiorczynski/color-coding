"""Generators of data for testing."""
import networkx as nx

def erdos_renyi_graph(n, p, seed=None):
    """Generates a random graph with n nodes and probability p of an edge between any two nodes."""
    graph = nx.erdos_renyi_graph(n, p, seed)
    return graph

def barabasi_albert_graph(n, m, seed=None):
    """Generates a random graph with n nodes by attaching new nodes each with m edges that are preferentially attached to existing nodes with high degree."""
    graph = nx.barabasi_albert_graph(n, m, seed)
    return graph

def watts_strogatz_graph(n, k, p, seed=None):
    """Generates a random graph with n nodes and k nearest neighbors for each node, and rewires edges with probability p."""
    graph = nx.watts_strogatz_graph(n, k, p, seed)
    return graph

def random_tree(k, seed=None):
    """Generates a random tree with k nodes."""
    tree = nx.random_tree(k, seed)
    return tree

def complete_graph(n, seed=None):
    """Generates a complete graph with n nodes."""
    graph = nx.complete_graph(n)
    return graph

def random_bipartite(m, n, p, seed=None):
    """Generates a random bipartiate graph with m nodes in one partition, n nodes in the other partition, and probability p
    of an edge between any two nodes."""
    graph = nx.bipartite.random_graph(m, n, p, seed)
    return graph