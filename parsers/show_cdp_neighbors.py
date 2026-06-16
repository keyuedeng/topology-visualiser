from ntc_templates.parse import parse_output

def parse_cdp_neighbors(raw_output: str) -> list:
    parsed_output = parse_output(
        platform="cisco_ios",
        command="show cdp neighbors detail", 
        data=raw_output
    )
    res = []
    for neighbor in parsed_output:
        res.append(
            {
                "neighbor": neighbor["neighbor_name"],
                "neighbor_ip": neighbor["mgmt_address"],
                "local_interface": neighbor["local_interface"],
                "remote_interface": neighbor["neighbor_interface"],
                "platform": neighbor["platform"].removeprefix("cisco ")
            }
        )
    return res