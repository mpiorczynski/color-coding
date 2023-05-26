import itertools
import networkx as nx


def find_isomorphic_subgraph(graph, input_graph):
    """
    Function solves isomorphic subgraph problem (brute force approach).
    :param graph: graph in which we are looking for an isomorphic subgraph
    :param input_graph: graph isomorphic to the subgraph we are looking for
    :return: isomorphic subgraph or None
    """
    nodes = list(graph.nodes())
    input_nodes = list(input_graph.nodes())
    input_size = len(input_nodes)

    # Generate all possible combinations of nodes for subgraph of input size
    combinations = itertools.combinations(nodes, input_size)
    for combination in combinations:
        subgraph = graph.subgraph(combination)
        if nx.is_isomorphic(subgraph, input_graph):
            return subgraph
    return None


if __name__ == '__main__':
    # Example usage
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])
    G.add_edges_from([(5, 6), (6, 7), (7, 8), (8, 5)])

    input_G = nx.Graph()
    input_G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

    isomorphic_subgraph = find_isomorphic_subgraph(G, input_G)
    if isomorphic_subgraph:
        print("Isomorphic subgraph found:")
        print("Nodes: " + str(isomorphic_subgraph.nodes()))
        print("Edges: " + str(isomorphic_subgraph.edges()))
    else:
        print("No isomorphic subgraph found.")
