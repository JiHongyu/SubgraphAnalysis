import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

from itertools import product


def core_useful(g, g_core):

    nodes = set(g.nodes())
    core_nodes = set(g_core.nodes())
    non_core_nodes = nodes - core_nodes
    shortest_path = nx.shortest_path(g)
    core_num = g_core.number_of_nodes()
    w = 0
    for x, y in product(tuple(non_core_nodes), tuple(non_core_nodes)):
        path = set(shortest_path[x][y])
        w += len(path & core_nodes)

    w /= core_num
    return w


def net_degree(g):
    ori_degree = g.degree().items()
    degree = defaultdict(int)
    for k in ori_degree:
        pass
    pass

g = nx.read_gexf(r'./result/ca_fav_motif_betweenness/ca_fav_motif_0.gexf')
g1= nx.read_gexf(r'./result/ca_fav_motif_betweenness/ca_fav_motif_1.gexf')

pr = nx.betweenness_centrality(g)
pr_list = list(pr.items())
pr_list.sort(key=lambda x:x[1],reverse=True)
nodes = [x[0] for x in pr_list[:g1.number_of_nodes()]]
g2 = g.subgraph(nodes)

w1 = core_useful(g, g1)
w2 = core_useful(g, g2)

print(w1)
print(w2)
