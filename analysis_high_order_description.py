from mlcd_interface import *
import mnets
import networkx as nx
from itertools import product, combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def generate_random_graph_paras(graph_generator, motifs_dict, order: int, times=10):

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
        cur_val_seq = {x: 0 for x in motifs_dict.keys()}
        graph = graph_generator()
        nodes = graph.nodes()
        for sub_nodes in combinations(nodes, order):
            sub_g = graph.subgraph(sub_nodes)
            for key in motifs_dict.keys():
                motif = motifs_dict[key]
                if nx.is_isomorphic(sub_g, motif):
                    cur_val_seq[key] += 1
                    break

        for key in motifs_dict.keys():
            all_val_seq[key].append(cur_val_seq[key])

    res = {x: (0, 0) for x in motifs_dict.keys()}

    for key in motifs_dict.keys():
        val_seq = all_val_seq[key]
        res[key][0] = np.sum(val_seq)/times
        res[key][1] = np.var(val_seq)

    return res


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

g = nx.Graph()
g.add_cycle([1,2,3,4,5,6,7,8,9,0])

g2 = find_neighbor_subgraph(g, 1, 2)

