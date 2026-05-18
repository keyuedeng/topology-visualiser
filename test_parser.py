from parsers.cdp_neighbours import parse_cdp_file
from graph import build_graph

filepath = 'samples/sample_cdp_border3850.txt'
devices = parse_cdp_file(filepath)
print(devices)

G = build_graph(devices, 'BORDER-3850-R8')
print("Nodes:", G.nodes())
print("Edges:", G.edges())
