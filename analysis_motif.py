from mlcd_interface import *
import mnets
import networkx as nx
from itertools import product, combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

# 网络测试

networks = [nx.Graph()]

input_cmd = mnets.lfr_cmd(n=100, k=10, maxk=30, mu=0.1, t1=2.5, on=5, om=2)
# 生成测试网络
print('生成测试网络数据')
lfr_benchmark = mnets.lfr_mn_benchmark(input_cmd, num_of_layer=3)

networks = lfr_benchmark['networks']

# 聚合网络
aggregative_net = nx.Graph()

for net in networks:
    aggregative_net.add_nodes_from(net.nodes())
    aggregative_net.add_edges_from(net.edges())

# 构建 motif

# No.1
m1 = nx.Graph()
m1.add_edges_from([(1,2),(2,3)])

# No.2
m2 = nx.Graph()
m2.add_edges_from([(1,2),(2,3),(1,3)])

ms = (m1, m2, )
ms_cnt = defaultdict(list)

# 网络节点 Core Number 统计
core_cnt = nx.core_number(aggregative_net)

core_nodes = defaultdict(list)
core_nodes[0] = []
for k in core_cnt:
    core_nodes[core_cnt[k]].append(k)


# 搜索不同 Core 下的聚合网络的 Motif，进行计数统计

core_nums = list(core_nodes.keys())
core_nums.sort()

for x in core_nodes.keys():

    k_shell = core_nodes[x]
    if len(k_shell) > 0:
        aggregative_net.remove_nodes_from(k_shell)
    nodes = aggregative_net.nodes()

    ms_cur_cnt = {x: 0 for x in range(len(ms))}

    for sub_nodes in combinations(nodes, 3):

        sub_g = aggregative_net.subgraph(sub_nodes)

        for y in range(len(ms)):
            mx = ms[y]
            if nx.is_isomorphic(sub_g, mx):
                ms_cur_cnt[y] += 1
                break

    for y in ms_cur_cnt:
        ms_cnt[y].append(ms_cur_cnt[y])

df = pd.DataFrame(data=ms_cnt)

