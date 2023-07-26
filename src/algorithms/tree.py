"""Implementation of classic rooted tree structure for constant time tree splitting in color coding algorithm."""
import copy 
from typing import List, Any
import networkx as nx
import random


class Tree:
    def __init__(self, root: int, children: List[Any]):
        self.root = root
        self.children = children
        self.nodes = self.update_nodes()
    

    def update_nodes(self):
        for child in self.children:
            child.update_nodes()

        self.nodes = {self.root}
        for child in self.children:
            self.nodes = set.union(self.nodes, child.nodes)

    def add(self, subtree):
        self.children.append(subtree)
        self.nodes = set.union(self.nodes, subtree.nodes)
    
    @staticmethod
    def from_networkx(nx_tree: nx.Graph):
        root = random.choice(list(nx_tree.nodes))

        # BFS
        queue = []
        visited = set()
        queue.append(root)
        visited.add(root)

        tree_root = Tree(root=root, children=[])
        tree_dict = {root: tree_root}

        while queue:
            current_node = queue.pop(0)

            for neighbor in nx_tree.neighbors(current_node):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    
                    subtree_root = Tree(root=neighbor, children=[])
                    tree_dict[neighbor] = subtree_root
                    tree_dict[current_node].children.append(subtree_root)
        
        
        tree_root.update_nodes()

        return tree_root

    
    def random_split(self):
        root_neighbor = random.choice(range(len(self.children)))
        subtree1 = copy.deepcopy(self)
        subtree2 = subtree1.children.pop(root_neighbor)
        subtree1.nodes = subtree1.nodes.difference(subtree2.nodes)
        return subtree1, subtree2
    

    def to_networkx(self) -> nx.Graph:
        tree = nx.Graph()

        if not self.children:
            tree.add_node(self.root)
        else:
            queue = []
            queue.append(self)

            while queue:
                current_node = queue.pop(0)
                for child in current_node.children:
                    queue.append(child)
                    tree.add_edge(current_node.root, child.root)

        return tree
    
    def number_of_nodes(self):
        return len(self.nodes)

    def __repr__(self) -> str:
        return f"Tree(root={self.root}, children={self.children})"