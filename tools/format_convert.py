import networkx as nx
import igraph as ig

def nx2ig(g_nx:nx.Graph):

    path = 'temp/nx2ig_temp.gml'

    nx.write_gml(g_nx, path=path)

    return ig.Graph.Read_GML(path)

