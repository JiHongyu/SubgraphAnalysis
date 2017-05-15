from analysis_high_order_description import *

target = ' 2196678548L'
filename = r'./result/ca_fav_motif_0.gexf'

g = nx.read_gexf(filename)
nodes_rank = nx.pagerank(g)
n_g = find_neighbor_subgraph(g, target, k=2)

opt_z = find_optimal_motif_type(
    n_g, motifs_count_v3, ms.mu4_c_dict, 4, 100
)
print('Motif: %s, Z-Score: %.4f' % (opt_z[0], opt_z[1]))

# 在显著 Motif 里面找一个最优的 Motif
print('find motif nodes')
best_motif_edges = find_opt_motif_instance_v2(n_g, ms.mu4_c_dict, 4, opt_z[0], nodes_rank)
