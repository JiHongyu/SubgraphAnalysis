from analysis_high_order_description import *
from pylouvain import *
import pandas as pd

def compute_paras(g):
    num_node = g.number_of_nodes()
    num_edge = g.number_of_edges()
    avg_degr = 2*num_edge/num_node


    components = [x for x in nx.connected_component_subgraphs(g, copy=False) if x.number_of_nodes() > 2]

    # 计算直径
    diameter = max((nx.diameter(x) for x in components))

    # 计算平均距离

    c_num_nodes = [x.number_of_nodes() for x in components]
    c_ave_dis = []
    for x in components:
        ave_dis = nx.average_shortest_path_length(x)
        c_ave_dis.append(ave_dis)

    _t = 0
    for x, y in zip(c_num_nodes, c_ave_dis):
        _t += y*x*(x-1)

    avg_dis = _t/num_node/(num_node-1)
    _,q = LouvainCommunities(g)
    avg_clr =  nx.average_clustering(g)

    return (num_node, num_edge, avg_degr, q, diameter, avg_dis, avg_clr)



n = 200
m = 2
p = 0.2
k = 4

# 节点，边，平均度，模块度，网络直径，平均距离，聚类系数
col = ['node', 'edge', 'degree', 'q', 'dim', 'dis', 'clr']
ori_data = []
cis_data = []
pr_data = []
for x in range(10):

    # 读入网络数据
    g = nx.powerlaw_cluster_graph(n, m, p)
    # 计算PageRank
    nodes_rank = nx.pagerank(g)

    # CIS网络
    core_edges = set()

    # 每个节点的邻域子图计算
    cnt = 0
    for n in g.nodes_iter():

        cnt += 1
        print('---------------------------------------------------')
        s_time = time.time()
        print('processing %d-----%d/%d' % (x, cnt, g.number_of_nodes()))

        # 获取邻域子图
        neighbor_sub_g = find_neighbor_subgraph(g, n, k=2)
        print('nodes: %s, edges: %s' % (neighbor_sub_g.number_of_nodes(),
                                        neighbor_sub_g.number_of_edges())
              )

        # 过滤与 Motif 同阶的邻域子图
        # if neighbor_sub_g.number_of_nodes() < order + 1:
        #     continue

        if neighbor_sub_g.number_of_nodes() < 30:
            mc_func = motifs_count
            find_opt_motif_instance_func = find_opt_motif_instance
        else:
            mc_func = motifs_count_v3
            find_opt_motif_instance_func = find_opt_motif_instance_v2

        # 寻找最显著 Motif
        print('Search optimal motif')
        opt_z = find_optimal_motif_type(
            neighbor_sub_g, mc_func, ms.mu3_c_dict, 3, 10
        )
        print('Motif: %s, Z-Score: %.4f' % (opt_z[0], opt_z[1]))

        # 在显著 Motif 里面找一个最优的 Motif
        print('find motif nodes')
        best_motif_edges = find_opt_motif_instance_func(neighbor_sub_g, ms.mu3_c_dict, 3, opt_z[0], nodes_rank)
        if best_motif_edges is not None:
            core_edges.update(best_motif_edges)

        e_time = time.time()
        print('Spend time %.3f' % (e_time - s_time))

    # 生成 Motif Core 网络
    g_motif_core = nx.Graph()
    g_motif_core.add_edges_from(core_edges)

    paras = compute_paras(g_motif_core)
    cis_data.append(paras)

    # 原始网络
    paras = compute_paras(g)
    ori_data.append(paras)

    # PR网络
    pr_list = list(nodes_rank.items())
    pr_list.sort(key=lambda x: x[1], reverse=True)
    nodes = [x[0] for x in pr_list[:g_motif_core.number_of_nodes()]]
    pr_g = g.subgraph(nodes)
    paras = compute_paras(pr_g)
    pr_data.append(paras)

df1 = pd.DataFrame(ori_data, columns=col)
df2 = pd.DataFrame(cis_data, columns=col)
df3 = pd.DataFrame(pr_data, columns=col)

