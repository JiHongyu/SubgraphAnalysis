import networkx as nx

g = nx.read_gexf(r'./result/sat_re_fa_p_motif_0.gexf')

idx = dict()

cnt = 0
for x in g.nodes_iter():
    idx[x] = cnt
    cnt += 1

with open(r'./result/fanmod.txt', 'w') as f:
    for x, y in g.edges_iter():
        f.write('%s %s\n' % (idx[x], idx[y]))

print('finish')
