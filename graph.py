import networkx as nx

def build_graph(parsed_data, seed_hostname):
    G = nx.Graph()
    for entry in parsed_data:
        device = entry['DEVICE_ID']
        local_int = entry['LOCAL_INTERFACE']
        remote_int = entry['REMOTE_INTERFACE']
        G.add_edge(seed_hostname, device, local_interface=local_int, remote_interface=remote_int)
        G.add_node(device, ip_address=entry['IP_ADDRESS'])
    return G
