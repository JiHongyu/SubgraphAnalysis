import networkx as nx
import numpy.random as random

def randomwalk(g:nx.Graph, number_of_nodes):

    if g.number_of_nodes() <= number_of_nodes:
        return g

    selected_set = set()

    cur_node = random.choice(g.nodes())
    selected_set.add(cur_node)

    over = 0

    cnt = 0
    while len(selected_set) < number_of_nodes:

        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(selected_set))
        neighbors = g.neighbors(cur_node)
        cur_node = random.choice(neighbors)

        if cur_node in selected_set:
            over += 1
        else:
            selected_set.add(cur_node)
            over = 0

        if over > 100:
            cur_node = random.choice(list(selected_set))

    return nx.subgraph(g, selected_set)

g = nx.read_gexf(r'result/sat_re_fa/sat_re_fa_p_motif_0.gexf')

for x in range(10):
    rw = randomwalk(g, 2650)
    nx.write_gexf(rw, './result/sat_re_fa_rw_%d.gexf'%x)

