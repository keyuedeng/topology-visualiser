from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Device:
    id: int
    hostname: str
    ips: set = field(default_factory=set)
    serial: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    confirmed: bool = False


def find(parent: dict, x: str) -> str:
    root = x
    while parent[root] != root:
        root = parent[root]

    # path compression: point every node on the walk directly at the root
    while parent[x] != root:
        parent[x], x = root, parent[x]

    return root


def union(parent: dict, x: str, y: str) -> str:
    root_x = find(parent, x)
    root_y = find(parent, y)

    if root_x != root_y:
        parent[root_y] = root_x

    return root_x

