import collections
import networkx as nx
import igraph as ig
import tools

import louvain

from .algo_base import Algorithm

class Louvain(Algorithm):

    def __init__(self, networks):

        Algorithm.__init__(self, networks)
        self.networks_ig = []
        for net in networks:
            self.networks_ig.append(tools.nx2ig(net))


    def run_algo(self, method):

        louvain_layers = []
        for net in self.networks_ig:
            layer = louvain.Layer(net, method)
            louvain_layers.append(layer)

        membership, quality = louvain.find_partition_multiplex(
            layers=louvain_layers, consider_comms=louvain.ALL_COMMS)

        com2node = collections.defaultdict(list)

        for n in range(len(membership)):
            c = membership[n]
            com2node[c].append(n)

        self.r['node_coms'] = tuple(x for x in com2node.values())
        self.r['com2node'] = com2node

        return self.r



