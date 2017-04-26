import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from sklearn import linear_model
from itertools import product
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def core_useful(g, g_core):

    nodes = set(g.nodes())
    core_nodes = set(g_core.nodes())
    non_core_nodes = nodes - core_nodes
    shortest_path = nx.shortest_path(g)
    core_num = g_core.number_of_nodes()
    w = 0
    for x, y in product(tuple(non_core_nodes), tuple(non_core_nodes)):
        path = set(shortest_path[x][y])
        w += len(path & core_nodes)

    w /= core_num
    return w


def net_degree_distribution(g):
    ori_degree = g.degree()
    degree = defaultdict(int)
    for k in ori_degree:
        degree[ori_degree[k]] += 1
    degree_distri = list(degree.items())
    degree_distri.sort(key=lambda x:x[0])
    x = [x[0] for x in degree_distri if x[0] != 0]
    y = [x[1] for x in degree_distri if x[0] != 0]
    logx = np.log2(x)
    logy = np.log2(y)
    plt.scatter(logx, logy)
    return degree_distri

def linear_regress(degree_distri):

    x = [x[0] for x in degree_distri if x[0] != 0]
    y = [x[1] for x in degree_distri if x[0] != 0]
    logx = np.log2(x)
    logy = np.log2(y)
    xdata = [[x] for x in logx]
    ydata = [[y] for y in logy]
    reg = linear_model.LinearRegression()
    reg.fit(xdata, ydata)
    pred_y = reg.predict(xdata)
    print('实验结论')
    print(reg.coef_)
    print(reg.residues_)
    print(reg.intercept_)
    plt.plot(logx, pred_y, '--', color='red', linewidth=1)
    threshold = [x for x in range(8)]
    group_labels = [2**x for x in threshold]
    plt.xticks(threshold, group_labels, rotation=0)
    ylist = [x for x in range(0,10,2)]
    plt.yticks([x for x in ylist], [2**x for x in ylist], rotation=0)


name = 'ws_motif'
g = nx.read_gexf(r'./result/%s_0.gexf' % name)
g1= nx.read_gexf(r'./result/%s_1.gexf' % name)

# pr = nx.betweenness_centrality(g)
pr = nx.pagerank(g)
pr_list = list(pr.items())
pr_list.sort(key=lambda x:x[1],reverse=True)
nodes = [x[0] for x in pr_list[:g1.number_of_nodes()]]
g2 = g.subgraph(nodes)

nx.write_gexf(g2, r'./result/%s_top_pagerank.gexf' % name)
w1 = core_useful(g, g1)
w2 = core_useful(g, g2)

print(w1)
print(w2)

plt.figure(1, figsize=(4, 3))
d = net_degree_distribution(g=g)
linear_regress(d[0:-4])
# linear_regress(d[1:])
plt.xlabel('节点度', fontsize=12)
plt.ylabel('度分布数量', fontsize=12)
plt.savefig(r'./result/%s_d1.pdf' % name)

plt.figure(2, figsize=(4, 3))
d = net_degree_distribution(g=g1)
linear_regress(d[1:-7])
plt.xlabel('节点度', fontsize=12)
plt.ylabel('度分布数量', fontsize=12)
plt.savefig(r'./result/%s_d2.pdf' % name)


plt.figure(3, figsize=(4, 3))
d = net_degree_distribution(g=g2)
linear_regress(d[2:-6])
plt.xlabel('节点度', fontsize=12)
plt.ylabel('度分布数量', fontsize=12)
plt.savefig(r'./result/%s_d3.pdf' % name)
plt.show()
