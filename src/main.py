"""Run isomorphic subtree search."""
import networkx as nx
from src.algorithms.subtree_isomorphism import IsomorphicSubtreeFinder
from src.utils import parse_args, print_config, set_seed, plot_graph_tree, read_graph
import time

def main():
    args = parse_args()
    set_seed(args.seed)

    # generate random graph using erdos renyi model
    if args.graph_path is None:
        graph = nx.erdos_renyi_graph(n=100, p=0.1, seed=args.seed)
    else:
        graph = read_graph(args.graph_path)

    # generate random tree
    tree = nx.random_tree(args.num_tree_nodes, seed=args.seed)

    # print config
    print_config(args.graph_path, graph.number_of_nodes(), graph.number_of_edges(), tree.number_of_nodes(), args.algorithm, args.seed)

    # plot graph and tree
    plot_graph_tree(graph, tree)

    start = time.perf_counter()
    finder = IsomorphicSubtreeFinder()
    found = finder.find(graph, tree, args.algorithm)
    end = time.perf_counter()
    runtime = end - start

    print(f"Isomorphic tree{'' if found else 'not'} found (elapsed time: {runtime}s)")
if __name__ == "__main__":
    main()
