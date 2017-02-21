
################################################
# 多网络连边社团检测算法的最优社团选择的目标函数，目标函数是寻找极大值
# 函数接口：
# networks：多网络列表；
# link_coms：边社团
# node_coms：点社团

def cuting_density(node_coms_num, link_coms_num, layer_num):
    min_com = node_coms_num - 1
    max_com = 0.5 * node_coms_num * (node_coms_num - 1)

    density = (link_coms_num - min_com) / (max_com - min_com) \
        if abs(max_com - min_com) > 0.0001 else 0

    return density

def objectfunc_by_mean(networks, link_coms, node_coms):

    cur_f = 0
    all_link_num = 0
    num_of_net = len(networks)
    for link_com, node_com in zip(link_coms, node_coms):

        # 计算社团在每一层的最大边数
        cur_com = 0
        for g in networks:
            for link in link_com:
                n1, n2 = link.node()
                if n2 in g.neighbors(n1):
                    cur_com += 1


        min_com = (len(node_com)-1)*num_of_net
        max_com = 0.5 * len(node_com) * (len(node_com) - 1)*num_of_net

        density = (cur_com-min_com)/(max_com-min_com) if abs(max_com-min_com) > 0.0001 else 0

        cur_f += cur_com * density
        all_link_num += cur_com

    return cur_f/all_link_num if all_link_num is not 0 else -1

def objectfunc_by_max(networks, link_coms, node_coms):
    cur_f = 0
    all_link_num = 0

    for link_com, node_com in zip(link_coms, node_coms):

        # 计算社团在每一层的最大边数
        cur_com = 0
        for g in networks:
            _t = 0
            for link in link_com:
                n1, n2 = link.node()
                if n2 in g.neighbors(n1):
                    _t += 1
            cur_com = max(cur_com, _t)

        min_com = (len(node_com) - 1)
        max_com = 0.5 * len(node_com) * (len(node_com) - 1)
        density = (cur_com-min_com)/(max_com-min_com) if abs(max_com-min_com) > 0.0001 else 0

        cur_f += cur_com * density
        all_link_num += cur_com

    return cur_f / all_link_num



