import networkx as nx

n = 100
m = 2
p = 0.2
k = 4
g1 = nx.powerlaw_cluster_graph(n, m, p)
nx.write_gexf(g1, r'./result/ba_100.gexf')

g2 = nx.watts_strogatz_graph(n, k, 0.2)
nx.write_gexf(g2, r'./result/ws_100.gexf')

print(g1.number_of_edges())
print(g2.number_of_edges())
