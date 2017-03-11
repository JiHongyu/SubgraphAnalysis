import networkx as nx
import matplotlib.pyplot as plt
import pickle
import pandas
import numpy as np
from collections import defaultdict

from itertools import product

#
# cluster_1 = (1, 2, 3, 4, 5, 6)
# cluster_2 = tuple((10*x for x in cluster_1))
#
# g = nx.Graph()
#
# g.add_edges_from(
#     [(x, y) for x, y in product(cluster_1, cluster_1) if x < y]
# )
# g.add_edges_from(
#     [(x, y) for x, y in product(cluster_2, cluster_2) if x < y]
# )
#
# # g.add_edge(1, 100)
# # g.add_edge(10, 100)
#
# g.add_edge(1, 10)
#
# nx.draw(g)
# plt.show()
# nx.write_gexf(g, 'test_2_motif_0.gexf')

import os
import pandas as pd
file_adapter = 'ca_fav_motif_%d.gexf'

data = []

for x in range(100):
    if not os.path.exists(file_adapter % x):
        break

    gx = nx.read_gexf(file_adapter % x)
    info = (gx.number_of_nodes(),
            gx.number_of_edges(),
            nx.number_connected_components(gx))

    data.append(info)

df = pd.DataFrame(data=data, columns=['node', 'edge', 'c'])


