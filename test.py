from mlcd_interface import *
import mnets
import networkx as nx
from itertools import product
import matplotlib.pyplot as plt

# 网络测试

networks = [nx.Graph()]

input_cmd = mnets.lfr_cmd(n=100, k=10, maxk=30, mu=0.1, t1=2.5, on=5, om=2)
# 生成测试网络
print('生成测试网络数据')
lfr_benchmark = mnets.lfr_mn_benchmark(input_cmd, num_of_layer=3)

networks = lfr_benchmark['networks']



mlcd_result = mlinkcoms_algo(networks, '')


ori_node_coms = mlcd_result['node_coms']

# 社团是否需要预处理

coms = [x for x in ori_node_coms if len(x) > 2]
coms_dict = {idx: x for x, idx in zip(coms, range(len(coms)))}

# 构建社团网络

com_net = nx.Graph()
for x in coms_dict:
    com_net.add_node(x, node_num=len(coms_dict[x]))

for x, y in product(coms_dict.keys(),coms_dict.keys()):
    if x < y:
        and_set = set(coms_dict[x]) & set(coms_dict[y])
        if len(and_set) > 0:
            t = len(and_set)/min(len(coms_dict[x]),len(coms_dict[y]))
            com_net.add_edge(x, y, weight=t)

nx.write_gexf(com_net, path='.\\result\\com_net.gexf')

bc = nx.betweenness_centrality(com_net, weight='weight')

b_s_data = []
for x in coms_dict.keys():
    b_s_data.append((len(coms_dict[x]), bc[x]))