from ntc_templates.parse import parse_output

def parse_show_version(raw_output: str) -> dict:
    parsed_output = parse_output(
        platform="cisco_ios",
        command="show version",
        data=raw_output
    )
    raw = parsed_output[0]
    return {
        "hostname": raw["hostname"],
        "version": raw["version"],
        "model": raw["hardware"][0] if raw["hardware"] else None,
        "serial": raw["serial"][0] if raw["serial"] else None
    }