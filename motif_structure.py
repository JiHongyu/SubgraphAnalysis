import networkx as nx

# 3阶无向 Motif
mu3_0 = nx.Graph(name='mu3_0')
mu3_0.add_edge(0, 1)
mu3_0.add_node(2)

mu3_1 = nx.Graph(name='mu3_1')
mu3_1.add_edges_from([(0, 1), (1, 2)])

mu3_2 = nx.Graph(name='mu3_2')
mu3_2.add_edges_from([(0, 1), (1, 2), (2, 0)])

mu3_list = [mu3_0, mu3_1, mu3_2]
mu3_dict = {x.name: x for x in mu3_list}

mu3_c_list = [mu3_1, mu3_2]
mu3_c_dict = {x.name: x for x in mu3_c_list}

# 4阶无向 Motif
mu4_0 = nx.Graph(name='mu4_0')
mu4_0.add_edge(1, 2)
mu4_0.add_nodes_from([0, 3])

mu4_1 = nx.Graph(name='mu4_1')
mu4_1.add_edges_from([(0, 3), (1, 2)])

mu4_2 = nx.Graph(name='mu4_2')
mu4_2.add_edges_from([(0, 1), (1, 2)])
mu4_2.add_node(3)

mu4_3 = nx.Graph(name='mu4_3')
mu4_3.add_edges_from([(0, 1), (1, 2), (2, 3)])

mu4_4 = nx.Graph(name='mu4_4')
mu4_4.add_edges_from([(0, 1), (1, 2), (2, 0)])
mu4_4.add_node(3)

mu4_5 = nx.Graph(name='mu4_5')
mu4_5.add_edges_from([(0, 1), (1, 2), (1, 3)])

mu4_6 = nx.Graph(name='mu4_6')
mu4_6.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

mu4_7 = nx.Graph(name='mu4_7')
mu4_7.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 1)])

mu4_8 = nx.Graph(name='mu4_8')
mu4_8.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)])

mu4_9 = nx.Graph(name='mu4_9')
mu4_9.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (0, 2)])

mu4_list = [mu4_0, mu4_1, mu4_2, mu4_3, mu4_4,
            mu4_5, mu4_6, mu4_7, mu4_8, mu4_9]
mu4_dict = {x.name: x for x in mu4_list}

mu4_c_list = [mu4_2, mu4_3, mu4_5, mu4_6,
              mu4_7, mu4_8, mu4_9]
mu4_c_dict = {x.name: x for x in mu4_c_list}

# 3阶有向 Motif

md3_0 = nx.DiGraph(name='md3_0')
md3_0.add_edges_from([(0, 1)])
md3_0.add_node(2)

md3_1 = nx.DiGraph(name='md3_1')
md3_1.add_edges_from([(0, 2), (2, 1), (1, 0)])

md3_2 = nx.DiGraph(name='md3_2')
md3_2.add_edges_from([(0, 2), (2, 1), (1, 0), (2, 0)])

md3_3 = nx.DiGraph(name='md3_3')
md3_3.add_edges_from([(0, 2), (2, 1), (1, 0), (2, 0), (1, 2)])

md3_4 = nx.DiGraph(name='md3_4')
md3_4.add_edges_from([(0, 2), (2, 1), (1, 0), (2, 0), (1, 2), (0, 1)])

md3_5 = nx.DiGraph(name='md3_5')
md3_5.add_edges_from([(0, 2), (1, 0), (1, 2)])

md3_6 = nx.DiGraph(name='md3_6')
md3_6.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 1)])

md3_7 = nx.DiGraph(name='md3_7')
md3_7.add_edges_from([(1, 0), (2, 0), (1, 2), (2, 1)])

md3_8 = nx.DiGraph(name='md3_8')
md3_8.add_edges_from([(0, 1), (0, 2)])

md3_9 = nx.DiGraph(name='md3_9')
md3_9.add_edges_from([(0, 1), (2, 0)])

md3_10 = nx.DiGraph(name='md3_10')
md3_10.add_edges_from([(1, 0), (2, 0)])

md3_11 = nx.DiGraph(name='md3_11')
md3_11.add_edges_from([(0, 1), (1, 0), (0, 2)])

md3_12 = nx.DiGraph(name='md3_12')
md3_12.add_edges_from([(0, 1), (1, 0), (2, 0)])

md3_13 = nx.DiGraph(name='md3_13')
md3_13.add_edges_from([(0, 1), (1, 0), (0, 2), (2, 0)])

md3_list = [md3_0, md3_1, md3_2, md3_3, md3_4, md3_5,
            md3_6, md3_7, md3_8, md3_9, md3_10,
            md3_11, md3_12, md3_13]

md3_dict = {x.name: x for x in md3_list}

# 4阶有向 Motif

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # for g in mu3_list:
    #     nx.draw(g)
    #     plt.show()
    #
    # for g in mu4_list:
    #     nx.draw(g)
    #     plt.show()
    #
    # for g in md3_list:
    #     nx.draw(g)
    #     plt.show()
