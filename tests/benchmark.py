"""Benchmark of implementations."""
from random import seed
import sys
import os
import time
import csv

PYTHON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(PYTHON_PATH)

from subtree_isomorphism import IsomorphicSubtreeFinder
from data_generation import erdos_renyi_graph, watts_strogatz_graph, barabasi_albert_graph, random_tree
from utils import set_seed, read_graph

SEED = 123
set_seed(SEED)

def benchmark(graph_path, tree_path):
    graph = read_graph(graph_path)
    tree = read_graph(tree_path)

    num_nodes = graph.number_of_nodes()
    num_tree_nodes = tree.number_of_nodes()

    finder = IsomorphicSubtreeFinder()

    start_time = time.time()
    cc_flag = finder.find(graph, tree, algorithm="color_coding")
    # calculate execution time for color coding
    ex_time_cc = time.time() - start_time
    
    start_time = time.time()
    bf_flag = finder.find(graph, tree, algorithm="brute_force")
    # calculate execution time for brute force
    ex_time_bf = time.time() - start_time

    return num_nodes, num_tree_nodes, graph_path, tree_path, bf_flag, cc_flag, ex_time_bf, ex_time_cc



if __name__ == "__main__":
    # define input graphs for benchmark 
    config = [
        (erdos_renyi_graph, {"n": 100, "p": 0.1, "seed": SEED}),
        (erdos_renyi_graph, {"n": 200, "p": 0.01, "seed": SEED}),
        (watts_strogatz_graph, {"n": 100, "k": 10, "p": 0.1, "seed": SEED}),
        (barabasi_albert_graph, {"n": 100, "m": 1, "seed": SEED}),
        (barabasi_albert_graph, {"n": 100, "m": 2, "seed": SEED}),
    ]

    with open("tests/benchmark.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "k", "graph_path", "tree_path", "bf_flag", "cc_flag", "time_bf", "time_cc"])

        for generator, kwargs in config:
            print(f"Running {generator.__name__} with {kwargs}")
            graph_path = generator(**kwargs)
            # graph_path = "data/ppi.edgelist"
            for k in range(3, 9):
                tree_path = random_tree(k, seed=SEED)
                ans = benchmark(graph_path, tree_path)
                # ans = benchmark(tree_path, tree_path)
                writer.writerow(ans)
                print(ans)