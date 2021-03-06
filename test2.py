# -*- coding: utf-8 -*-
from __future__ import division

# from mlcd_interface import *
# import mnets
import networkx as nx
from itertools import product, combinations
from collections import defaultdict
import matplotlib.pyplot as plt
# import pandas as pd
import numpy as np
import motif_structure as ms
from functools import partial
import time
import sys



def find_neighbor_nodes(network, target, k=1):

    # 结果
    res = set()
    # 当前待搜索节点集
    cur = {target}
    # 搜索过的节点集
    found = set()

    # 迭代搜索
    for x in range(k+1):
        # 保存数据
        res.update(cur)

        # 搜索下一跳
        nxt = set()
        for node in cur:
            nxt.update(network.neighbors_iter(node))
        # 更新搜索过得节点集
        found.update(cur)
        # 下一步迭代节点集
        cur = nxt.difference(found)

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

def motifs_count_v2(graph, motifs_dict, order):
    m_c = {x: [] for x in motifs_dict.keys()}
    t_nodes = graph.nodes()
    for sub_nodes in combinations(t_nodes, order):
        sub_g = graph.subgraph(sub_nodes)
        for key in motifs_dict.keys():
            motif = motifs_dict[key]
            if nx.is_isomorphic(sub_g, motif):
                m_c[key].append(sub_nodes)
                break
    return m_c

def generate_random_graph_paras(graph_generator, motifs_dict, order, times):

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
        res[key][1] = np.sqrt(res[key][1])

    return res


def find_optimal_motif_v1(graph, motifs_dict, order, times):
    t_nodes = graph.nodes()
    p = 2*graph.number_of_edges()/graph.number_of_nodes()/(graph.number_of_nodes()-1)
    er_g_f = partial(nx.fast_gnp_random_graph, n=len(t_nodes), p=p)
    er_p = generate_random_graph_paras(er_g_f, motifs_dict, order, times)

    m_c = motifs_count(graph, motifs_dict, order)

    z_score = []
    for k in motifs_dict:
        if abs(er_p[k][1]) < 0.001:
            val = (m_c[k] - er_p[k][0])
        else:
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
            yield sub_n, sub_g.edges()


def mining_motif_core(file_adapter, selector, motifs_dict, motif_order, neighbor_order, times, start, end):
    '''

    :param file_adapter: 文件名适配器
    :param selector: Motif 采样选择器
    :param motifs_dict: Motif 字典，由 motif_structure.py 内定义
    :param motif_order: Motif 阶数
    :param neighbor_order: 邻域子图阶数
    :param times: 随机模拟次数
    :param start: 起始迭代位置（闭区间）
    :param end: 终止迭代位置（开区间）
    :return: (文件输出)
    '''
    for x in range(start, end, 1):

        # 读入网络数据
        g = nx.read_gexf(file_adapter % x)
        # 计算PageRank
        nodes_rank = selector(g)

        core_edges = set()

        # 每个节点的邻域子图计算
        cnt = 0
        for n in g.nodes_iter():

            cnt += 1
            print('---------------------------------------------------')
            s_time = time.time()
            print('processing %d/%d' % (cnt, g.number_of_nodes()))

            # 获取邻域子图
            neighbor_sub_g = find_neighbor_subgraph(g, n, k=neighbor_order)
            print('nodes: %s, edges: %s' % (neighbor_sub_g.number_of_nodes(),
                                            neighbor_sub_g.number_of_edges())
                  )

            # 过滤与 Motif 同阶的邻域子图
            # if neighbor_sub_g.number_of_nodes() < order + 1:
            #     continue

            # 寻找最显著 Motif
            print('Search optimal motif')
            opt_z = find_optimal_motif_v1(
                neighbor_sub_g, motifs_dict, motif_order, times
            )
            print('Motif: %s, Z-Score: %.4f' % (opt_z[0], opt_z[1]))

            # 在显著 Motif 里面找一个最优的 Motif
            print('find motif nodes')
            best_motif_edges = None
            best_motif_val = 0.0001
            for m_nodes, m_edges in find_motifs(neighbor_sub_g,
                                                motifs_dict, motif_order, opt_z[0]):
                val = sum((nodes_rank[x] for x in m_nodes))
                if val > best_motif_val:
                    best_motif_edges = m_edges
                    best_motif_val = val
            if best_motif_edges is not None:
                core_edges.update(best_motif_edges)

            e_time = time.time()
            print('Spend time %.3f' % (e_time-s_time))

        # 生成 Motif Core 网络，并保存
        g_motif_core = nx.Graph()
        g_motif_core.add_edges_from(core_edges)
        nx.write_gexf(g_motif_core, file_adapter % (x+1))

if __name__ == '__main__':

    # centrality = nx.pagerank
    centrality = nx.betweenness_centrality
    # centrality = nx.communicability_centrality
    file_adapter = '.\\result\\karate_motif_%d.gexf'
    # file_adapter = '.\\result\\ws_motif_%d.gexf'
    motifs_dict = ms.mu3_c_dict
    order = 3
    neighbor_order = 2

    mining_motif_core(file_adapter=file_adapter,
                      selector=centrality,
                      motifs_dict=ms.mu3_c_dict,
                      motif_order=3,
                      neighbor_order=2,
                      times=20,
                      start=0,
                      end=4)
