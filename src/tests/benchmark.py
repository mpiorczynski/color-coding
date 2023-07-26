"""Benchmark of implementations."""
from random import seed
import sys
import os
import time
import csv
import networkx as nx

from src.algorithms.subtree_isomorphism import IsomorphicSubtreeFinder
from src.utils import set_seed, read_graph

SEED = 42
set_seed(SEED)

# GROUPS = ["barabasi_albert_graph", "random_bipartite", "complete_graph", "erdos_renyi_graph",
        #   "karate_club",  "random_tree", "watts_strogatz_graph"]
GROUPS = ["random_bipartite",]

def test_algorithms(graph_path: str, tree_path: str):
    graph = read_graph(graph_path)
    tree = read_graph(tree_path)

    num_nodes = graph.number_of_nodes()
    num_tree_nodes = tree.number_of_nodes()

    finder = IsomorphicSubtreeFinder()

    start_time = time.perf_counter()
    cc_flag = finder.find(graph, tree, algorithm="color_coding")
    # calculate execution time for color coding
    ex_time_cc = time.perf_counter() - start_time
    
    start_time = time.perf_counter()
    bf_flag = finder.find(graph, tree, algorithm="brute_force")
    # calculate execution time for brute force
    ex_time_bf = time.perf_counter() - start_time

    return num_nodes, num_tree_nodes, graph_path, tree_path, bf_flag, cc_flag, ex_time_bf, ex_time_cc

def main():
    for group in GROUPS:
        with open(f"results/{group}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["n", "k", "graph_path", "tree_path", "bf_flag", "cc_flag", "time_bf", "time_cc"])
            for graph_file in os.listdir(f"data/{group}"):
                graph_path = os.path.join(f"data/{group}", graph_file)
                for tree_file in os.listdir("data/random_tree"):
                    tree_path = os.path.join("data/random_tree", tree_file)

                    print(f"Looking for {tree_path} in {graph_path}.")
                    ans = test_algorithms(graph_path, tree_path)
                    writer.writerow(ans)

        print("====================================")




if __name__ == "__main__":
    main()