import textfsm
import json

def parse_cdp_file(filepath):
    # open files
    with open(filepath) as data, open('parsers/cdp_neighbours.textfsm') as template_file:
        raw_output = data.read()
        textfsm_parser = textfsm.TextFSM(template_file)
        parsed_data = textfsm_parser.ParseText(raw_output)
        parsed_output = [dict(zip(textfsm_parser.header,row)) for row in parsed_data]
    return parsed_output