import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G):
    labels = {}
    for node, attrs in G.nodes(data=True):
        if attrs.get('ip_address'):
            labels[node] = f"{node}\n{attrs.get('ip_address')}"
        else:
            labels[node] = node

    plt.figure(figsize=(14, 10))
    nx.draw(G, labels=labels, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10, font_weight='bold')
    plt.show()