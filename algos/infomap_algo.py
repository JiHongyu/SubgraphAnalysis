import itertools
import collections
import os
from .algo_base import Algorithm


class Infomap(Algorithm):

    def __init__(self, networks, path:str=None, name=None):
        Algorithm.__init__(self, networks)

        # 建立网络索引
        layer = 0
        self.net_idx = {}
        for net in networks:
            layer += 1
            self.net_idx[net] = layer

        # 建立节点索引
        self.nodes = networks[0].nodes()
        num_of_nodes = len(self.nodes)
        self.node_idx = {x: x+1 for x in self.nodes}
        self.node_ridx = {x+1: x for x in self.nodes}
        if path is None:
            self.path = ''
        else:
            self.path = path
        if name is None:
            self.name = 'tmp'
        else:
            self.name = name

    def run_algo(self, paras='--clu'):
        self.__save_mn_pajek_v1()
        self.__run_exec_file(paras=paras)
        self.__analyze_file_result()
        return self.r

    def __save_mn_pajek_v1(self):

        networks = self.networks

        # 1. 构建节点信息
        context = []
        context.append('*Vertices %s \n'%len(self.nodes))
        for n in self.nodes:
            context.append( '%s \"%s\" \n'%(self.node_idx[n], n))

        # 2. 构建网络信息
        context.append('*Multiplex \n' )

        # 2.1 构建同层网络信息

        s = '%s %s %s %s 1 \n'

        for net in networks:
            layer = self.net_idx[net]
            for n1, n2 in net.edges():
                context.append(s % (layer, self.node_idx[n1], layer, self.node_idx[n2]))
                context.append(s % (layer, self.node_idx[n2], layer, self.node_idx[n1]))

        # 2.2 构建跨层网络信息
        for net1, net2 in itertools.product(networks, networks):

            if net1 is net2:
                continue
            l1 = self.net_idx[net1]
            l2 = self.net_idx[net2]
            for n in self.nodes:
                context.append(s % (l1, self.node_idx[n], l2, self.node_idx[n]))
                context.append(s % (l2, self.node_idx[n], l1, self.node_idx[n]))

        #  写入文件
        path = '%s%s.net'%(self.path,self.name)
        with open(path , 'w') as f:
            f.writelines(context)

    def __run_exec_file(self, paras):

        infomap_cmd = 'Infomap %s %s%s.net %s -i multiplex' % \
                   (paras, self.path, self.name, self.path)
        os.system(infomap_cmd)



    def __analyze_file_result(self):

        path = '%s%s.clu' % (self.path, self.name)
        node2com = collections.defaultdict(list)
        com2node = collections.defaultdict(list)
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                data = line.split()
                node2com[self.node_ridx[int(data[0])]].append(int(data[1]))
                com2node[int(data[1])].append(self.node_ridx[int(data[0])])

        self.r['node_coms'] = tuple(x for x in com2node.values())
        self.r['node2com'] = node2com
        self.r['com2node'] = com2node


