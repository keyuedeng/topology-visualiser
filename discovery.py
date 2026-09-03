from collections import deque

from connection import connect
from device import find
from parsers.show_cdp_neighbors import parse_cdp_neighbors
from parsers.show_lldp_neighbors import parse_lldp_neighbors
from parsers.show_version import parse_show_version
from registry import DeviceRegistry


def discover_topology(seed_ip, username, password, secret):
    registry = DeviceRegistry()
    edges = []
    visited = set()

    seed_device = registry.register_neighbor(hostname="unknown", ip=seed_ip)
    queue = deque([seed_device.id])

    while queue:
        current_id = queue.popleft()
        canonical_id = find(registry.parent, current_id)

        if canonical_id in visited:
            continue
        visited.add(canonical_id)

        device = registry.devices[canonical_id]
        ip = next(iter(device.ips))

        conn = connect(ip, username, password, secret)

        version_info = parse_show_version(conn.send_command("show version"))
        device = registry.confirm_device(
            canonical_id, 
            serial=version_info["serial"],
            model=version_info["model"],
            version=version_info["version"],
        )
        device.hostname = version_info["hostname"]
        cdp_neighbors = parse_cdp_neighbors(conn.send_command("show cdp neighbors detail"))
        lldp_neighbors = parse_lldp_neighbors(conn.send_command("show lldp neighbors detail"))
        conn.disconnect()

        for neighbor in cdp_neighbors + lldp_neighbors:
            neighbor_device = registry.register_neighbor(
                hostname=neighbor["neighbor"],
                ip=neighbor["neighbor_ip"],
            )
            edges.append({
                "local_device": device.id,
                "remote_device": neighbor_device.id,
                "local_interface": neighbor["local_interface"],
                "remote_interface": neighbor["remote_interface"],
                "ip": neighbor["neighbor_ip"],
            })

            if neighbor["neighbor_ip"]:
                queue.append(neighbor_device.id)

    return registry, edges


