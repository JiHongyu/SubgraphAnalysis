import networkx as nx

g1 = nx.read_gexf(r'./result/ca_fav0.gexf')
g2 = nx.read_gexf(r'./result/ca_retw0.gexf')
g3 = nx.read_gexf(r'./result/ca_conv0.gexf')

n1 = set(g1.nodes())
n2 = set(g2.nodes())
n3 = set(g3.nodes())

n = (n1 & n2) & n3

sg1 = g1.subgraph(n1 & n)
sg2 = g2.subgraph(n2 & n)
sg3 = g3.subgraph(n3 & n)

nx.write_gexf(sg1, r'./result/ca_m_fav.gexf')
nx.write_gexf(sg2, r'./result/ca_m_retw.gexf')
nx.write_gexf(sg3, r'./result/ca_m_conv.gexf')
