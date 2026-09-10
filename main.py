import argparse

from connection import get_credentials
from discovery import discover_topology
from graph import build_graph
from preview import preview
from drawio_export import export_to_drawio


def main():
    parser = argparse.ArgumentParser(description="Discover and visualise a network topology via CDP/LLDP.")
    parser.add_argument("--seed", required=True, help="IP address of the seed device to start discovery from")
    args = parser.parse_args()

    username, password, secret = get_credentials()

    registry, edges = discover_topology(args.seed, username, password, secret)
    G = build_graph(registry, edges)

    output_path = "topology.drawio"
    export_to_drawio(G, registry, output_path)

    print(f"\nDiscovered {len(registry.devices)} devices and {len(edges)} edges")
    print(f"Diagram saved to {output_path}")

    preview(G, registry)


if __name__ == "__main__":
    main()
