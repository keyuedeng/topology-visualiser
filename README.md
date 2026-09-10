# Topology Visualiser

A CDP/LLDP-based physical topology discovery tool — maps device-to-device cabling and produces a draw.io diagram.

SSHes into a seed network device, recursively discovers the topology via CDP and LLDP, and exports a draw.io diagram (plus a quick matplotlib preview).

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python main.py --seed <ip>
```

`<ip>` is the management IP of any single device to start discovery from.

You'll be prompted for:
- **Username**
- **Password**
- **Enable secret** — press Enter to reuse the login password if it's the same

The same credentials are used for every device discovered during the run. Devices that reject them, or that are unreachable from wherever you're running this, are skipped and left as unconfirmed (gray) nodes rather than stopping the whole run — see `DEV_NOTES.md` for details.

While it runs, progress prints to the terminal (`Connecting to ...`, `Confirmed ...`, `Unreachable, skipping: ...`) — this can take a while on a large topology, especially if several devices are unreachable (each one waits out a real ~10s timeout before moving on).

## Output

- **`topology.drawio`** — the primary output, saved in the current directory. Open it in the [draw.io app](https://www.diagrams.net/) or at [diagrams.net](https://app.diagrams.net/). Hover over a device to see its IP, model, IOS version, and serial number. Each link is labeled on both ends with the local/remote interface.
- **A matplotlib preview window** — pops up after the file is saved, as a quick visual sanity check. Closing it doesn't affect the saved file.

### Cleaning up the layout

Node positions are computed automatically, but on a larger topology they can end up cramped or overlapping. After opening `topology.drawio`, run **Arrange → Layout → Vertical Flow** (or **Organic**) from the draw.io menu to auto-arrange the diagram — this only takes one click and consistently gives a much cleaner result than the initial auto-generated layout.

## Known limitations

See `DEV_NOTES.md` for the full list of accepted limitations and design tradeoffs (e.g. devices with no management IP can appear as duplicate nodes, only one shared credential set is used per run).
