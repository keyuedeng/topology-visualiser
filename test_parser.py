from parsers.cdp_neighbours import parse_cdp_file

filepath = 'samples/sample_cdp_border3850.txt'
devices = parse_cdp_file(filepath)
print(devices)
