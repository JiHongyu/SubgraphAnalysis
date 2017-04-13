import networkx as nx

n = 100
m = 1
p = 0.3

g = nx.powerlaw_cluster_graph(n, m, p)

nx.write_gexf(g, r'./result/ba_2.gexf')