import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from sklearn import linear_model
from itertools import product
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def core_useful(g, g_core, shortest_path):

    # 全部节点
    nodes = set(g.nodes())
    # 核心结构节点
    core_nodes = set(g_core.nodes())
    # 非核心结构节点
    non_core_nodes = nodes - core_nodes
    # 核心节点个数
    core_node_num = g_core.number_of_nodes()
    # 核心结构边数
    core_edge_num = g_core.number_of_edges()
    w = 0
    for x, y in product(tuple(non_core_nodes), tuple(non_core_nodes)):
        path = set(shortest_path[x][y])
        w += len(path & core_nodes)

    w /= core_node_num
    if core_edge_num != 0:
        w /= core_edge_num
    return w

def near_core(g, g_core, shortest_path):

    # 全部节点
    nodes = set(g.nodes())
    # 核心结构节点
    core_nodes = set(g_core.nodes())
    # 非核心结构节点
    non_core_nodes = nodes - core_nodes
    # 核心节点个数
    core_node_num = g_core.number_of_nodes()
    # 核心结构边数
    core_edge_num = g_core.number_of_edges()

    w = 0
    for x in non_core_nodes:
        dis_n = shortest_path[x]
        core_dis = [(x, len(dis_n[x])) for x in dis_n if x in core_nodes]
        if len(core_dis) == 0:
            continue
        core_dis.sort(key=lambda x:x[1])
        w += core_dis[0][1]

    if core_edge_num == 0:
        core_edge_num = 1

    #w *= core_node_num/core_edge_num
    w *= core_edge_num/(core_node_num)
    return w


def cal_avg_degree(g):
    degree_seqs = g.degree().values()
    return sum((x*x for x in degree_seqs))/g.number_of_nodes()

name = r'result/random_test/hk_3/ba_motif'
g_ori = nx.nx.read_gexf(r'%s_0.gexf' % name)
g1 = nx.read_gexf(r'%s_0.gexf' % name)
g2= nx.read_gexf(r'%s_1.gexf' % name)
shortest_path = nx.shortest_path(g1)

# 计算高阶平均度
k2_g1 = cal_avg_degree(g1)
k2_g2 = cal_avg_degree(g2)

print('g1, ', k2_g1)
print('g2, ', k2_g2)

# END

print('计算核心影响网络')
w0 = near_core(g1, g2, shortest_path)

pr = nx.pagerank(g1)
pr_list = list(pr.items())
pr_list.sort(key=lambda x: x[1], reverse=True)
pr_nodes = [x[0] for x in pr_list]

print('计算中心性网络')
pr_ws = []
for x in range(1, len(pr_nodes)+1):
    if x%10 == 0:
        print(x)
    pr_g = g1.subgraph(pr_nodes[:x])
    w = near_core(g1, pr_g, shortest_path)
    pr_ws.append(w)

plt.scatter([x for x in range(1, len(pr_nodes)+1)], pr_ws)
plt.scatter(g2.number_of_nodes(), w0)
plt.show()

