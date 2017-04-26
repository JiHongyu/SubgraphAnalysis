import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from itertools import product
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

from collections import defaultdict
from itertools import product
#
# g = nx.Graph()
# tweet_user = defaultdict(list)
#
# with open(r'state_fav_result.txt') as f:
#     for line in f:
#         ori_data = line[1:-2]
#         tweet, user = tuple(ori_data.split())
#         tweet_user[tweet].append(user)
#         g.add_edge(tweet, user)
#         g.node[tweet]['T'] = 'tweet'
#         g.node[user]['T'] = 'user'
#
# nx.write_gexf(g, r'./result/ca_fav_213123123.gexf')
#
# g = nx.Graph()
#
# for tweet in tweet_user:
#     user_list = tweet_user[tweet]
#     edges = ((x, y) for x, y in product(user_list, user_list) if x != y)
#     g.add_edges_from(edges)
#
# nx.write_gexf(g, r'./result/ca_fav_complete.gexf')

g = nx.read_gexf(r'./result/sat_re_fa.gexf')

components = nx.connected_component_subgraphs(g)

node_nums = []
edge_nums = []
data_nums = []
components_list = [x for x in components]
components_list.sort(key=lambda x:x.number_of_nodes(), reverse=True)
for subg in components_list:
    if subg.number_of_nodes() > 3:
        a = subg.number_of_nodes()
        b = subg.number_of_edges()
        node_nums.append(a)
        edge_nums.append(b)
        data_nums.append((a,b,))

xdata = [x for x in range(len(node_nums))]
# ax = plt.figure(1)
#
# plt.scatter(xdata, node_nums)
# plt.scatter(xdata, edge_nums)
# # plt.semilogy(node_nums)
# # plt.semilogy(edge_nums)
# plt.yscale('log')
#
# plt.show()

df = pd.DataFrame(data_nums, columns=['节点','边'])

df.plot.bar(figsize=(5, 4), log=True, fontsize=10.5)
plt.xlabel('连通分支编号', fontsize=10.5)
plt.ylabel('数量', fontsize=10.5)
plt.savefig(r'./result/sat_re_fa_component.pdf')
plt.show()

g1 = components_list[0]
