import networkx as nx
import pandas as pd

from graph import *
from max_flow import * 



def run_exp(k=5, verbose=False):
    g = Graph()
    g.add_nodes(["s"] + [ str(i+1) for i in range(k) ] + [ f"{str(i+1)}'" for i in range(k) ] + ["t"])

    for i in range(k):
        g.add_edge("s", str(i+1), {"capacity" : 2})
        g.add_edge(f"{str(i+1)}'", "t", {"capacity" : 1})

        for j in range(k):
            g.add_edge(str(i+1), f"{str(j+1)}'", {"capacity" : 999999})



    stats = solve_max_flow(g, g.get_node("s"), g.get_node("t"), verbose=verbose)
    print(f'MAX FLOW: {g.get_node("t").excess}')
    return stats

if __name__ == '__main__':
    print(run_exp(k=1, verbose=True))
