"""Test for Naive Implementation"""
import pandas as pd
import networkx as nx
import sys
import os
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(folder_path)
import src.naive_implementation as cc
import src.brute_force as bf

def test(n, k, p, seed):
    # generate random graph using erdos renyi model
    graph = nx.erdos_renyi_graph(n, p, seed)
    # generate random tree
    tree = nx.random_tree(k, seed)
    # assume brute force returns correct solution
    corr = bf.find_isomorphic_subtree(graph, tree)
    ans = cc.color_coding(graph, tree)
    flag = ans == corr
    return n, k, p, corr, ans, flag

def many_tests(ns, ks, ps, seed):
    ans = []
    for n in ns:
        for k in ks:
            for p in ps:
                ans.append(test(n, k, p/10, seed))
    return ans

def make_df(ans):
    df = pd.DataFrame(ans, columns=["n", "k", "p", "correct", "answear", "flag"])
    return df

if __name__ == "__main__":
    seed = 1337
    ns = range(3, 15, 1)
    ks = range(2, 8, 1)
    ps = range(0, 10, 1)
    # perform tests
    ans = many_tests(ns, ks, ps, seed)
    df = make_df(ans)
    # save dataframe
    df.to_csv('./data/test_naive_implementation.csv')