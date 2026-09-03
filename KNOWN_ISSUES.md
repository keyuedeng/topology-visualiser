# Known issues / possible improvements

Running list of gaps and design tradeoffs found while testing against the real lab. Not all of these need fixing — some are accepted limitations — but worth tracking so they don't get forgotten.

## Identity / deduplication

- **No-IP devices (e.g. ESXi hosts) can appear as duplicate nodes.** Devices with no CDP/LLDP management address (no serial either, since we never connect to them) have no reliable identity key, so the same physical host discovered from two different neighbors becomes two separate `Device` records. Confirmed happening in the real lab (`an-esxi-host`, `an-esxi-host`-`an-esxi-host`, etc. each appeared twice). Accepted limitation for now — fixing this would need a different identity signal for these devices (MAC address via LLDP chassis ID, maybe).
- **Union-Find merge logic hasn't been exercised against real data yet.** Every multi-IP device seen in real lab output (`a-wan-router`, `another-wan-router`, etc.) happened to be unreachable, so `confirm_device`'s merge branch never actually ran outside of reasoning/design. Worth revisiting once a real multi-IP device is reachable, to confirm the merge behaves as designed.

## Connectivity / credentials

- **Single credential set for the whole traversal.** `discover_topology` takes one username/password/secret and reuses it for every device. Real lab testing showed 3 devices reject those creds (`a-switch`, `a-switch`, `a-gateway-device`) — currently treated the same as unreachable (skipped, left unconfirmed). Worth checking whether this is expected (different admin domain) or a gap before investing in multi-credential support.
- **Arbitrary IP selection when a device has multiple known IPs.** `ip = next(iter(device.ips))` in `discovery.py` picks one from an unordered set — no logic to retry a different known IP if the chosen one fails to connect.
- **Only two exception types caught around `connect()`/`send_command()`.** `NetmikoTimeoutException` and `NetmikoAuthenticationException` are handled; other failure modes (e.g. a command hanging after a successful connection) aren't specifically handled yet.

## Not yet built

- draw.io XML export
- matplotlib quick preview
- CLI wiring (`argparse --seed`) in `main.py`

## Rendering limitations

- **matplotlib quick preview doesn't offset parallel edges.** Since the graph is a `MultiGraph`, two separate physical links between the same pair of devices (e.g. the `another-wan-router` double-link case) are stored correctly as two distinct edges, but `nx.draw()` doesn't visually separate them — they'll overlap and look like a single line in the quick preview. Acceptable for a fast sanity-check tool; the draw.io export can do better (e.g. curved/offset lines) since it's the primary output.

## Future improvements (out of original scope)

- **EtherChannel/port-channel bundles aren't detected.** CDP/LLDP report per physical member interface, so a multi-link EtherChannel between two devices currently shows up as multiple independent parallel edges (handled correctly, since `MultiGraph` supports this) but with no indication they're actually one logical bundle. Detecting this would need a new parser + an additional command (`show etherchannel summary` or similar) to group member interfaces together. Deferred until the core deliverables (draw.io export, matplotlib preview, CLI) are done.
