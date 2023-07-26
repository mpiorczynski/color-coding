"""Generate data for testing."""
import os
import sys

import networkx as nx

from src.graphs.graphs_generators import (barabasi_albert_graph, complete_graph,
                                      erdos_renyi_graph, random_bipartite,
                                      random_tree, watts_strogatz_graph)
from src.utils import save_graph, set_seed

SEED = 123
set_seed(SEED)
CONFIG = (
    [
        (watts_strogatz_graph, {"n": 100, "k": 10, "p": 0.1, "seed": SEED}),
        (barabasi_albert_graph, {"n": 100, "m": 1, "seed": SEED}),
        (barabasi_albert_graph, {"n": 100, "m": 2, "seed": SEED}),
        (erdos_renyi_graph, {"n": 100, "p": 0.1, "seed": SEED}),
    ]
    + [
        (erdos_renyi_graph, {"n": n, "p": 2 / n, "seed": SEED})
        for n in [20, 50, 100, 200, 500]
    ]
    + [(random_tree, {"k": k, "seed": SEED}) for k in range(3, 15)]
    + [(complete_graph, {"n": n, "seed": SEED}) for n in [25, 50, 100, 200]]
    + [(random_bipartite, {"m": m, "n": n, "p": 0.5, "seed": SEED}) for m, n in [(10, 10), (20, 20), (50, 50)]]
)



def path_template(generator, kwargs):
    return f"data/{generator.__name__}/{generator.__name__}_{'_'.join([str(kwargs[key]) for key in kwargs])}.edgelist"

def main():
    for generator, kwargs in CONFIG:
        print(f"Running {generator.__name__} with {kwargs}")
        path = path_template(generator, kwargs)
        graph = generator(**kwargs)
        save_graph(graph, path)

if __name__ == "__main__":
    main()