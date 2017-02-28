import networkx as nx
from itertools import product
import pandas as pd
import collections

filename = 'state_fav_result.txt'

info = collections.defaultdict(list)

raw_data = []
cnt = 0
with open(filename, 'r') as f:
    for line in f:
        cnt += 1
        t = line[1:-2]
        data = t.split(',')
        info[data[0]].append(data[1])
        raw_data.append((data[0], data[1]))
    print('Read %s lines' % cnt)

g1 = nx.Graph()
for k in info:
    nodes = info[k]
    edges = ((x, y) for x, y in product(nodes, nodes) if x != y)
    g1.add_edges_from(edges)


g2 = nx.Graph()
for k in info:
    nodes = info[k]
    g2.add_edges_from(product([k], nodes))
    g2.node[k]['t'] = 'twitter'
    for n in nodes:
        g2.node[n]['t'] = 'user'


max_cpt = [0, None]
for g in nx.connected_component_subgraphs(g1):
    if g.number_of_nodes() > max_cpt[0]:
        max_cpt[0] = g.number_of_nodes()
        max_cpt[1] = g

g1 = max_cpt[1]

nx.write_gexf(g1, '.\\result\\g1.gexf')
nx.write_gexf(g2, '.\\result\\g2.gexf')
