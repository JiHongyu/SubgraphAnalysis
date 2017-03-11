import networkx as nx
import os
import matplotlib.pyplot as plt
import pickle
import pandas
import numpy as np
from collections import defaultdict


# pg = nx.pagerank(g1)
# pg2 = list(pg.items())
# pg2.sort(key=lambda x:x[1], reverse=True)
# toppg = pg2[0:g2.number_of_nodes()]
# topnode = [x for x,y in toppg]
#
# n1 = set()
# n2 = set()
#
# for n in g2.nodes():
#     n1.update(g1.neighbors(n))
#
# for n in topnode:
#     n2.update(g1.neighbors(n))
#
# core = nx.core_number(g1)
# core_node = list(core.items())
# core_node.sort(key=lambda x:x[1], reverse=True)
# core_k_dict = defaultdict(int)
# for n, k in core_node:
#     core_k_dict[k] += 1
#
# top_core_k = core_node[0][1]
# top_core = [x for x, y in core_node if y == top_core_k]

file_adapter = 'pw_motif_%d.gexf'

g1 = nx.read_gexf(file_adapter % 0)

for n in g1.nodes():
    g1.node[n]['sample'] = 0
for x in range(1, 100):
    if not os.path.exists(file_adapter % x):
        break
    gx = nx.read_gexf(file_adapter % x)
    for n in gx.nodes():
        g1.node[n]['sample'] = x

nx.write_gexf(g1, 'pw_motif_core_aly.gexf')



