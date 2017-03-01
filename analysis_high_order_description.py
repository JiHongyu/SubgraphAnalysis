# -*- coding: utf-8 -*-

# from mlcd_interface import *
# import mnets
import networkx as nx
from itertools import product, combinations
from collections import defaultdict
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
import motif_structure as ms
from functools import partial


def find_neighbor_nodes(network, target, k=1):

    # 结果
    res = set()
    # 当前待搜索节点集
    cur = {target}
    # 搜索过的节点集
    found = set()

    # 迭代搜索
    for x in range(k+1):
        # 搜索下一跳
        nxt = set()
        for node in cur:
            if node not in found:
                nxt.update(network.neighbors_iter(node))
        # 更新搜索过得节点集
        found.update(cur)
        # 下一步迭代节点集
        cur = nxt
        # 保存数据
        res.update(cur)
    return tuple(res)


def find_neighbor_subgraph(network, target, k=1):

    nodes = find_neighbor_nodes(network, target, k)

    return network.subgraph(nodes)


def motifs_count(graph, motifs_dict, order):
    m_c = {x: 0 for x in motifs_dict.keys()}
    t_nodes = graph.nodes()
    for sub_nodes in combinations(t_nodes, order):
        sub_g = graph.subgraph(sub_nodes)
        for key in motifs_dict.keys():
            motif = motifs_dict[key]
            if nx.is_isomorphic(sub_g, motif):
                m_c[key] += 1
                break
    return m_c


def generate_random_graph_paras(graph_generator, motifs_dict, order, times=4):

    '''
    参考论文：Local Topology of Social Network Based on Motif Analysis
    :param graph_generator: 网络生成函数
    :param motifs_dict:  motif 字典
    :param order: Motif 阶数
    :param times:  随机网络次数
    :return: motif 参数字典，键：motif_dict键，值：(期望，方差)
    '''

    all_val_seq = defaultdict(list)

    for x in range(times):

        graph = graph_generator()

        cur_val_seq = motifs_count(graph, motifs_dict, order)

        for key in motifs_dict.keys():
            all_val_seq[key].append(cur_val_seq[key])

    res = {x: [0, 0] for x in motifs_dict.keys()}

    for key in motifs_dict.keys():
        val_seq = all_val_seq[key]
        res[key][0] = sum(val_seq)/times
        res[key][1] = sum((x**2 for x in val_seq))/times - res[key][0]

    return res


def find_optimal_motif_v1(graph, motifs_dict, order):
    t_nodes = graph.nodes()
    er_g_f = partial(nx.fast_gnp_random_graph, n=len(t_nodes), p=0.3)
    er_p = generate_random_graph_paras(er_g_f, motifs_dict, order)

    m_c = motifs_count(graph, motifs_dict, order)

    z_score = []
    for k in motifs_dict:
        val = (m_c[k] - er_p[k][0])/er_p[k][1]
        z_score.append([k, val])

    z_score.sort(key=lambda x: x[1], reverse=True)
    return z_score[0]


def find_motifs(graph, motifs_dict, order, target_mf_k):

    t_nodes = graph.nodes()
    target_motif = motifs_dict[target_mf_k]

    for sub_n in combinations(t_nodes, order):
        sub_g = graph.subgraph(sub_n)
        if nx.is_isomorphic(sub_g, target_motif):
            yield sub_n


g = nx.read_gexf('.\\result\\ca_f.gexf')

motifs_dict = ms.mu3_c_dict
order = 3

nodes = g.nodes()

core_nodes = set()

cnt = 0

for n in nodes:

    cnt += 1

    print('-----------------------------')
    print('iterater %d' % cnt)

    neighbor_sub_g = find_neighbor_subgraph(g, n, k=2)

    print('nodes: %s, edges: %s' % (neighbor_sub_g.number_of_nodes(),
                                    neighbor_sub_g.number_of_edges())
          )
    print('Search optimal motif')
    opt_z = find_optimal_motif_v1(
        neighbor_sub_g, motifs_dict, order
    )
    print('%s, %d' % (opt_z[0], opt_z[1]))

    print('find motif nodes')
    for m_nodes in find_motifs(neighbor_sub_g,
                             motifs_dict, order, opt_z[0]):
        core_nodes.update(m_nodes)

core_g = g.subgraph(core_nodes)

nx.write_gexf(core_g, '.\\result\\ca_f_core1.gexf')







