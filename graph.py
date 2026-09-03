import networkx as nx

from device import find


def build_graph(registry, edges):
    G = nx.MultiGraph()

    for device_id, device in registry.devices.items():
        G.add_node(
            device_id,
            hostname=device.hostname,
            ips=device.ips,
            model=device.model,
            version=device.version,
            serial=device.serial,
        )

    for edge in edges:
        local_id = find(registry.parent, edge["local_device"])
        remote_id = find(registry.parent, edge["remote_device"])

        G.add_edge(
            local_id,
            remote_id,
            local_interface=edge["local_interface"],
            remote_interface=edge["remote_interface"],
            ip=edge["ip"],
        )

    return G
