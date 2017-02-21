from functools import partial
from itertools import product
import networkx as nx
from .edge import Edge


class MNetwork:

    def __init__(self, networks: [nx.Graph]):

        # 对每层未命名的网络命名
        idx = 1
        for net in networks:
            if net.name == '':
                net.name = 't%s' % idx
                idx += 1

        # 初始化多网络数据
        self.networksList = networks
        self.networksDict = {x.name: x for x in networks}
        self.networksName = set((x.name for x in networks))

        # 初始化 project 网络
        self.projectNetwork = nx.Graph(name="fusion net")
        self.projectLinkpair = nx.Graph(name="fusion linkpair")

        for graph in self.networksList:
            self.projectNetwork.add_nodes_from(graph.nodes())
            self.projectNetwork.add_edges_from(graph.edges())

        # 算法相关
        # 连边相似性计算算法
        self.linkpair_simi_func = None
        # 最优社团划分目标函数
        self.object_func = None

    def linkpairs(self):
        """提取融合后的单网络中的所有具有公共邻居的边对
        """

        # _linkpair = set()  # {(a,b,c)...}
        # for src, dst in self.project_nets.edges():
        #
        #     for src_neighbors in self.project_nets.neighbors(src):
        #         if src_neighbors < dst:
        #             _linkpair.add((src_neighbors, src, dst,))
        #         elif src_neighbors > dst:
        #             _linkpair.add((dst, src, src_neighbors,))
        #         else:
        #             pass
        #
        #     for dst_neighbors in self.project_nets.neighbors(dst):
        #         if dst_neighbors < src:
        #             _linkpair.add((dst_neighbors, dst, src,))
        #         elif dst_neighbors > src:
        #             _linkpair.add((src, dst, dst_neighbors,))
        #         else:
        #             pass

        _linkpair = []

        for mid in self.project_nets.nodes_iter():
            neighbors = self.project_nets.neighbors(mid)
            for x in range(len(neighbors)):
                for y in range(x+1,len(neighbors)):
                    _linkpair.append((neighbors[x], mid, neighbors[y]))
        return _linkpair

    def link_similarity_table(self):

        linkpairs = self.linkpairs()
        linkpair_similarity = []

        linkpair_num = len(linkpairs)

        cnt = 0
        for src, mid, dst in linkpairs:
            cnt += 1
            if ( cnt%50000 == 0):
                print('计算相似性 %5d/%5d'%(cnt, linkpair_num))
            # 计算相似性
            simi = self.linkpair_simi_func(src=src, mid=mid, dst=dst)

            # 用自定义数据结构存储连边对和对应的相似性
            link1 = Edge(src, mid)
            link2 = Edge(mid, dst)
            linkpair_similarity.append((link1, link2, simi))

        # 相似性排序并返回
        linkpair_similarity.sort(key=lambda x: x[2], reverse=True)

        return linkpair_similarity

    def nodes(self):

        return list(self.projectNetwork.nodes())

    def links(self):
        _links = list()

        for n1, n2 in self.projectNetwork.edges():
            _links.append(Edge(n1, n2))

        return _links

    def objectfunc(self, link_coms, node_coms):

        return self.object_func(link_coms=link_coms, node_coms=node_coms)

    def set_linkpair_simi_algo(self, algo_func):

        self.linkpair_simi_func = \
            partial(algo_func, networks=self.networksList)

    def set_objectfunc_algo(self, algo_func):
        self.object_func = \
            partial(algo_func, networks=self.networksList)

    @property
    def project_nets(self):
        return self.projectNetwork

    @property
    def project_linkpairs(self):
        return self.projectLinkpair







