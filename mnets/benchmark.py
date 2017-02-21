import os
import collections
import copy
import time

import networkx as nx
#from numpy import random
import random


def cmd_cache(func):

    def inner(*args, **kwargs):
        pass
    pass


def lfr_cmd(n, k, maxk, mu, **kwargs):

    cmd = '-N %s -k %s -maxk %s -mu %s' %\
           (n, k, maxk, mu)

    parameters = ['t1', 't2', 'minc', 'maxc', 'on', 'om']

    for p in parameters:
        if p in kwargs:
            cmd += ' -%s %s' % (p, kwargs[p])

    return cmd

def gn_cmd(mu):

    return lfr_cmd(128, 16, 16, mu, minc=32, maxc=32)

def process_original_lfr_data(name='L1'):

    g = nx.Graph(name=name)

    com2node = collections.defaultdict(list)
    node2com = collections.defaultdict(list)
    # 处理 benchamrk 网络数据，网络用 nx.Graph 结构存储
    with open('network.dat', 'r') as f:
        for line in f:
            _t = line.split()
            g.add_edge(int(_t[0])-1, int(_t[1])-1)

    # 处理 benchmark 社团数据，社团存储为社团集合
    with open('community.dat', 'r') as f:
        for line in f:
            _t = line.split()
            n = int(_t[0])-1
            for c in _t[1:]:
                com2node[c].append(n)
                node2com[n].append(c)

    #com2node = tuple(com2node.values())

    # 其他东西带不考虑

    d = dict()
    d['network'] = g
    d['com2node'] = com2node
    d['node2com'] = node2com
    d['nodes'] = tuple(node2com.keys())
    return d

def lfr_sn_benchmark(command:str, is_new=True):

    if is_new:
        os.system('lfr %s' % command)

    net_info = process_original_lfr_data(name='single network')

    g = net_info['network']
    node2com = net_info['node2com']



    return net_info

def gn_sn_benchmark(mu:float = 0.1):


    return lfr_sn_benchmark(gn_cmd(mu))


def rewire_benchmark(g: nx.Graph, com2node: dict, node2com: dict):

    # rewiring links without destroying structure of the network
    random.seed(int(time.time()))

    #com_cnt = {x:len(com2node[x])/4 for x in com2node.keys()}
    com_cnt = {x: 10 for x in com2node.keys()}
    # rewire inner links
    rand_nodes = g.nodes()
    random.shuffle(rand_nodes)
    for x1 in rand_nodes:

        # 节点所属的社团
        in_coms = node2com[x1]
        # 随机选择其中一个社团
        com = random.choice(in_coms)

        if com_cnt[com] < 1:
            continue
        else:
            com_cnt[com] -= 1

        # 选择与 x1 相邻的社团内节点 x2，构成边 x1--x2
        _t = list(set(g.neighbors(x1)) & set(com2node[com]))
        if len(_t) < 1:
            continue
        x2 = random.choice(_t)

        # 选择与 x1 在一个社团的边 y1--y2
        y1 = random.choice(com2node[com])
        _t = list(set(g.neighbors(y1)) & set(com2node[com]))
        if len(_t) < 1:
            continue
        y2 = random.choice(_t)

        # 交换边对节点 x1--x2, y1--y2
        _t = list({x1, x2, y1, y2})

        if len(_t) == 4 and x1 not in g.neighbors(y2) and x2 not in g.neighbors(y1):
            g.remove_edges_from([(x1, x2), (y1, y2)])
            g.add_edges_from([(x1, y2), (x2, y1)])
        else:
            pass

    # rewire outer links
    rand_nodes = g.nodes()
    random.shuffle(rand_nodes)
    for x1 in rand_nodes:

        # 节点所属的社团
        in_coms = node2com[x1]
        # 随机选择其中一个社团
        com = random.choice(in_coms)

        # 选择与 x1 相邻的社团外节点 x2，构成边 x1--x2
        _t = list(set(g.neighbors(x1)) - set(com2node[com]))
        if len(_t) < 1:
            continue
        x2 = random.choice(_t)

        # 选择与 x1 在一个社团的节点 y1 的外边 y1--y2
        y1 = random.choice(com2node[com])
        _t = list(set(g.neighbors(y1)) - set(com2node[com]))
        if len(_t) < 1:
            continue
        y2 = random.choice(_t)

        _c = 0# random.randint(0,1)


        if x1 is not y1:
            g.remove_edges_from([(x1, x2), (y1, y2)])
            if _c == 0:
                # 交换边对节点 x1--x2, y1--y2
                g.add_edges_from([(x1, y2), (x2, y1)])
            else:
                g.add_nodes_from([x1, x2, y1, y2])




def lfr_mn_benchmark(command:str, num_of_layer:int):

    lfr = lfr_sn_benchmark(command)

    g_ori = lfr['network']
    com2node = lfr['com2node']
    node2com = lfr['node2com']

    networks = []

    for layer in range(num_of_layer):
        g = copy.deepcopy(g_ori)
        rewire_benchmark(g, com2node, node2com)
        networks.append(g)

    lfr['networks'] = networks
    lfr.pop('network')

    return lfr


def gn_mn_benchmark(num_of_layer: int, mu:float= 0.1):

    return lfr_mn_benchmark(gn_cmd(mu), num_of_layer)


if __name__ == '__main__':
    pass
