import networkx as nx
from subtree_isomorphism import IsomorphicSubtreeFinder
from utils import parse_args, print_config, set_seed, plot_graph_tree

def main():
    """
    Parsing command line parameters, reading data, find subtree, save to file.
    """
    args = parse_args()
    set_seed(args.seed)

    # generate random graph using erdos renyi model
    graph = nx.erdos_renyi_graph(args.n, p=args.n/1000, seed=args.seed)
    # graph = read_graph("data/cora.edgelist")

    # generate random tree
    tree = nx.random_tree(args.k, seed=args.seed)

    # print config
    print_config(graph.number_of_nodes(), graph.number_of_edges(), tree.number_of_nodes(), args.algorithm, args.seed)

    # plot graph and tree
    plot_graph_tree(graph, tree)

    finder = IsomorphicSubtreeFinder()
    flag = finder.find(graph, tree, args.algorithm)

    print(f"Is there a subtree with {args.k} vertices in the graph with {args.n} vertices?: {flag}")

if __name__ == "__main__":
    main()
