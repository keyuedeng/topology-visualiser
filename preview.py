import matplotlib.pyplot as plt
import networkx as nx


def preview(G, registry):
    pos = nx.spring_layout(G)
    labels = {device_id: device.hostname for device_id, device in registry.devices.items()}

    nx.draw(
        G,
        pos,
        labels=labels,
        with_labels=True,
        node_color="lightblue",
        node_size=300,
        font_size=6,
    )
    plt.show()
