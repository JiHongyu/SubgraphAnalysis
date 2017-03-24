import networkx as nx
from collections import defaultdict
from itertools import product

g = nx.Graph()
tweet_user = defaultdict(list)

with open(r'state_fav_result.txt') as f:
    for line in f:
        ori_data = line[1:-2]
        tweet, user = tuple(ori_data.split())
        tweet_user[tweet].append(user)
        g.add_edge(tweet, user)
        g.node[tweet]['T'] = 'tweet'
        g.node[user]['T'] = 'user'

nx.write_gexf(g, r'./result/ca_fav_213123123.gexf')

g = nx.Graph()

for tweet in tweet_user:
    user_list = tweet_user[tweet]
    edges = ((x, y) for x, y in product(user_list, user_list) if x != y)
    g.add_edges_from(edges)

nx.write_gexf(g, r'./result/ca_fav_complete.gexf')


