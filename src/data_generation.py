"""Generate data for testing."""
import networkx as nx

def add_selfloops_for_isolated(graph):
    """Utility function to add self loops to a graph to save isolated nodes in edgelist format."""
    isolated_nodes = [node for node in graph.nodes if graph.degree(node) == 0]
    for node in isolated_nodes:
        graph.add_edge(node, node)

def erdos_renyi_graph(n, p, seed=None):
    graph = nx.erdos_renyi_graph(n, p, seed)
    add_selfloops_for_isolated(graph)
    path = f"data/erdos_renyi_{n}_{p}_{seed}.edgelist"
    nx.write_edgelist(graph, path, delimiter=",", data=False)
    return path

def barabasi_albert_graph(n, m, seed=None):
    graph = nx.barabasi_albert_graph(n, m, seed)
    add_selfloops_for_isolated(graph)
    path = f"data/barabasi_albert_{n}_{m}_{seed}.edgelist"
    nx.write_edgelist(graph, path, delimiter=",", data=False)
    return path

def watts_strogatz_graph(n, k, p, seed=None):
    graph = nx.watts_strogatz_graph(n, k, p, seed)
    add_selfloops_for_isolated(graph)
    path = f"data/watts_strogatz_{n}_{k}_{p}_{seed}.edgelist"
    nx.write_edgelist(graph, path, delimiter=",", data=False)
    return path

def random_tree(k, seed=None):
    tree = nx.random_tree(k, seed)
    path = f"data/tree_{k}_{seed}.edgelist"
    nx.write_edgelist(tree, path, delimiter=",", data=False)
    return path
