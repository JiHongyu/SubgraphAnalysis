import itertools
import numpy as np
################################################
# 多网络连边相似性计算可选函数，后面的函数均需按照接口规范
# 函数接口：
# networks：多网络列表；
# src, mid, dst：依次是连边的起点，中间点，截止点；
# alpha：控制参数

def linkpair_simi_1(networks, src, mid, dst, alpha: float = 0.5):
    """ 计算节点相似性，原始方法，利用Jaccard度量方法
    输入: src, mid, dst: 边对标识符,alpha: 同层跨层控制系数
    输出: 节点相似性
    """
    # Case 1: complete src----mid----dst layers
    inlayer_src_neighbors = {src}
    inlayer_dst_neighbors = {dst}
    # Case 2: incomplete src--x--mid-----dst layers
    #          or        src-----mid--X--dst layers
    crslayer_src_neighbors = {src}
    crslayer_dst_neighbors = {dst}
    for graph in networks:
        if mid not in graph.nodes():
            continue

        if src in graph.neighbors(mid) and dst in graph.neighbors(mid):
            inlayer_src_neighbors.update(graph.neighbors(src))
            inlayer_dst_neighbors.update(graph.neighbors(dst))

        if src not in graph.neighbors(mid) and dst in graph.neighbors(mid):
            crslayer_src_neighbors.update(graph.neighbors(dst))

        if src in graph.neighbors(mid) and dst not in graph.neighbors(mid):
            crslayer_dst_neighbors.update(graph.neighbors(src))

    # Similarity
    # S1
    in_layer_simi = len(inlayer_src_neighbors & inlayer_dst_neighbors)\
                    / len(inlayer_src_neighbors | inlayer_dst_neighbors)
    # S2
    cross_layer_simi = len(crslayer_src_neighbors & crslayer_dst_neighbors)\
                       / len(crslayer_src_neighbors | crslayer_dst_neighbors)

    return (in_layer_simi + alpha * cross_layer_simi)/(1+alpha)


def linkpair_simi_2(networks, src, mid, dst, alpha: float = 0.5):

    inlayer_numerator = 0.0
    inlayer_denumerator = 0.0
    crslayer_numerator = 0.0
    crslayer_denumerator = 0.0

    num_of_nets = len(networks)

    # 同层计算
    for g1 in networks:
        inlayer_numerator += len(set(g1.neighbors(src)) & set(g1.neighbors(dst)))
        inlayer_denumerator += np.sqrt(len(g1.neighbors(src)) * len(g1.neighbors(dst)))

    # 跨层计算
    for x in range(num_of_nets-1):
        g1 = networks[x]
        for g2 in networks[x+1:]:
            crslayer_numerator += len(set(g1.neighbors(src)) & set(g2.neighbors(dst)))
            crslayer_denumerator += np.sqrt(len(g1.neighbors(src)) * len(g2.neighbors(dst)))

    if num_of_nets != 1:
        simi_num = inlayer_numerator + 2 * alpha * crslayer_numerator / (num_of_nets - 1)
        simi_den = inlayer_denumerator + 2 * alpha * crslayer_denumerator / (num_of_nets - 1)
    else:
        simi_num = inlayer_numerator
        simi_den = inlayer_denumerator

    return simi_num / simi_den if simi_den > 0.00001 else 0