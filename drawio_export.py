import xml.etree.ElementTree as ET

import networkx as nx

CANVAS_SCALE = 400
NODE_WIDTH = 140
NODE_HEIGHT = 60
CONFIRMED_COLOR = "#dae8fc"
UNCONFIRMED_COLOR = "#f5f5f5"


def export_to_drawio(G, registry, filepath):
    pos = nx.spring_layout(G)
    scaled_pos = {node: (x * CANVAS_SCALE, y * CANVAS_SCALE) for node, (x, y) in pos.items()}

    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram", name="Topology", id="topology-diagram")
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        dx="800", dy="600", grid="1", gridSize="10", guides="1",
        tooltips="1", connect="1", arrows="1", fold="1", page="1",
        pageScale="1", pageWidth="850", pageHeight="1100", math="0", shadow="0",
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    for device_id, device in registry.devices.items():
        node_id = f"node-{device_id}"
        x, y = scaled_pos[device_id]

        tooltip_lines = [f"IP: {', '.join(device.ips) or 'unknown'}"]
        if device.model:
            tooltip_lines.append(f"Model: {device.model}")
        if device.version:
            tooltip_lines.append(f"Version: {device.version}")
        if device.serial:
            tooltip_lines.append(f"Serial: {device.serial}")
        tooltip = "\n".join(tooltip_lines)

        fill_color = CONFIRMED_COLOR if device.confirmed else UNCONFIRMED_COLOR

        user_object = ET.SubElement(
            root, "UserObject",
            id=node_id, label=device.hostname, tooltip=tooltip,
        )
        cell = ET.SubElement(
            user_object, "mxCell",
            style=f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill_color};",
            vertex="1", parent="1",
        )
        ET.SubElement(
            cell, "mxGeometry",
            x=str(x), y=str(y), width=str(NODE_WIDTH), height=str(NODE_HEIGHT),
            **{"as": "geometry"},
        )

    for i, (u, v, key, data) in enumerate(G.edges(keys=True, data=True)):
        edge_id = f"edge-{i}"
        cell = ET.SubElement(
            root, "mxCell",
            id=edge_id,
            style="edgeStyle=orthogonalEdgeStyle;rounded=0;",
            edge="1", parent="1",
            source=f"node-{u}", target=f"node-{v}",
        )
        geometry = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})

        if key > 0:
            ux, uy = scaled_pos[u]
            vx, vy = scaled_pos[v]
            mx, my = (ux + vx) / 2, (uy + vy) / 2
            dx, dy = vx - ux, vy - uy
            length = (dx ** 2 + dy ** 2) ** 0.5 or 1
            perp_x, perp_y = -dy / length, dx / length
            offset = key * 30
            wx, wy = mx + perp_x * offset, my + perp_y * offset

            points = ET.SubElement(geometry, "Array", **{"as": "points"})
            ET.SubElement(points, "mxPoint", x=str(wx), y=str(wy))

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
