import networkx as nx
import pandas as pd

from graph import *
from max_flow import * 


k = 5
g = Graph()
g.add_nodes(["s"] + [ str(i+1) for i in range(k) ] + [ f"{str(i+1)}'" for i in range(k) ] + ["t"])

for i in range(k):
    g.add_edge("s", str(i+1), {"capacity" : 2})
    g.add_edge(f"{str(i+1)}'", "t", {"capacity" : 1})

    for j in range(k):
        g.add_edge(str(i+1), f"{str(i+1)}'", {"capacity" : 999999})




print(solve_max_flow(g, g.get_node("s"), g.get_node("t"), verbose=True))
#print(g)