import src.algorithms.color_coding as cc
import src.algorithms.brute_force as bf


class IsomorphicSubtreeFinder:
    def __init__(self) -> None:
        pass

    def find(self, graph, tree, algorithm="color_coding"):
        if algorithm == "color_coding":
            flag = cc.find_isomorphic_subtree(graph, tree)
        elif algorithm == "brute_force":
            flag = bf.find_isomorphic_subtree(graph, tree)
        else:
            raise NotImplementedError("Algorithm not implemented.")
    
        return flag
