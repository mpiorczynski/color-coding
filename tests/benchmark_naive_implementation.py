"""Benchmark for Naive Implementation"""
import pandas as pd
import networkx as nx
import time
import sys
import os
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(folder_path)
import src.naive_implementation as cc
import src.brute_force as bf

def benchmark(n, k, p, seed):
    # generate random graph using erdos renyi model
    graph = nx.erdos_renyi_graph(n, p, seed)
    # generate random tree
    tree = nx.random_tree(k, seed)
    start_time = time.time()
    ans = cc.color_coding(graph, tree)
    # calculate execution time for color coding
    ex_time_cc = time.time() - start_time
    start_time = time.time()
    corr = bf.find_isomorphic_subtree(graph, tree)
    # calculate execution time for brute force
    ex_time_bf = time.time() - start_time
    flag = ans == corr
    return n, k, p, corr, ans, flag, ex_time_bf, ex_time_cc

def many_benchmarks(ns, ks, ps, seed):
    ans = []
    for n in ns:
        for k in ks:
            for p in ps:
                ans.append(benchmark(n, k, p/10, seed))
    return ans

def make_df(ans):
    df = pd.DataFrame(ans, columns=["n", "k", "p", "correct", "answear", "flag", "time_bf", "time_cc"])
    return df

if __name__ == "__main__":
    seed = 1337
    ns = range(3, 15, 1)
    ks = range(2, 8, 1)
    ps = range(0, 10, 1)
    # perform benchmark
    ans = many_benchmarks(ns, ks, ps, seed)
    df = make_df(ans)
    # save dataframe
    df.to_csv('./data/benchmark_naive_implementation.csv')