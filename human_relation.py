import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
from itertools import product
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def cal_pr(g:nx.Graph):
    pr = nx.pagerank(g)
    pr_list = list(pr.items())
    pr_list.sort(key=lambda x: x[1], reverse=True)
    return pr_list

def compare_rank(g1:nx.Graph, g2:nx.Graph):
    pr_g1 = nx.pagerank(g1)
    pr_g2 = nx.pagerank(g2)

    pr_list = list(pr_g2.items())
    pr_list.sort(key=lambda x: x[1], reverse=True)
    cnt = int(g2.number_of_nodes()/10)
    pr_list = pr_list[:cnt]
    nodes = [x[0] for x in pr_list]

    cnt = 0
    for x, y in product(nodes, nodes):
        if pr_g1[x] < pr_g1[y] and pr_g2[x] < pr_g2[y]:
            cnt += 1

    return 2*cnt/len(nodes)/(len(nodes)-1)

def compare_top(g1:nx.Graph, g2:nx.Graph):

    pr_g1 = cal_pr(g1)
    pr_g2 = cal_pr(g2)

    num = len(pr_g2)

    s1 = set()
    s2 = set()

    simi_list = []
    for x in range(num):
        s1.add(pr_g1[x][0])
        s2.add(pr_g2[x][0])

        simi = len(s1 & s2)/len(s1)
        simi_list.append(simi)

    return simi_list


g0 = nx.read_gexf(r'./result/ca_fav_motif_0.gexf')
g1 = nx.read_gexf(r'./result/ca_fav_rw.gexf')
g2 = nx.read_gexf(r'./result/new/ca_fav_m_3_2/ca_fav_motif_1.gexf')
g3 = nx.read_gexf(r'./result/ca_fav_pr.gexf')

# g0 = nx.read_gexf(r'./result/sat_re_fa_p.gexf')
# g1 = nx.read_gexf(r'./result/sat_re_fa_rw.gexf')
# g2 = nx.read_gexf(r'./result/sat_re_fa/sat_re_fa_p_motif_1.gexf')

# for sg in nx.connected_component_subgraphs(g2):
#     if sg.number_of_nodes() > 1000:
#         g2 = sg
#         break
#
# g3 = nx.read_gexf(r'./result/sat_re_fa_p_pr.gexf')



print(compare_rank(g0, g2)) # Motif
print(compare_rank(g0, g1)) # RW
print(compare_rank(g0, g3)) # PR

y1 = compare_top(g0, g2)
y2 = compare_top(g0, g1)
y3 = compare_top(g0, g3)
plt.plot(y1, label='Motif')
plt.plot(y2, label='RW')
plt.plot(y3, label='PR')
plt.xlabel('Top 顶点数', fontsize=12)
plt.ylabel('相似度', fontsize=12)
plt.grid()
plt.legend()
plt.show()
