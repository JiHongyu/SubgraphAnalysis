import networkx as nx


def pr_network(g:nx.Graph, number_of_nodes):

    if g.number_of_nodes() <= number_of_nodes:
        return g

    pr = nx.pagerank(g)
    pr_list = list(pr.items())
    pr_list.sort(key=lambda x: x[1], reverse=True)

    nodes = [x[0] for x in pr_list[:number_of_nodes]]

    return g.subgraph(nodes)



g = nx.read_gexf(r'./result/sat_re_fa_p.gexf')

pr_g = pr_network(g, 2650)

nx.write_gexf(pr_g, r'./result/sat_re_fa_p_pr.gexf')
