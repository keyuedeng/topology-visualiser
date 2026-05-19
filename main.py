from parsers.cdp_neighbours import parse_cdp_file
from graph import build_graph
from visualiser import draw_graph

if __name__ == "__main__":
    filepath = 'samples/sample_cdp_border3850.txt'
    devices = parse_cdp_file(filepath)

    G = build_graph(devices, 'BORDER-3850-R8')
    draw_graph(G)
