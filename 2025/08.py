import math


def update_networks(networks: dict[int, set[int]], connection: tuple[int, int]):
    node1, node2 = connection
    root1 = next((k for k, nw in networks.items() if node1 in nw), None)
    root2 = next((k for k, nw in networks.items() if node2 in nw), None)

    if root1 is not None and root2 is not None:
        if root1 != root2:
            networks[root1] |= networks.pop(root2)
    elif root1 is not None:
        networks[root1].add(node2)
    elif root2 is not None:
        networks[root2].add(node1)
    else:
        networks[node1] = {node1, node2}


def run(input_data: str):
    part1, part2 = 0, 0

    input_lines = input_data.splitlines()
    NUM_CONNECTIONS = 1000 if len(input_lines) > 20 else 10
    box_list = [tuple(map(int, line.split(","))) for line in input_lines]
    distances: dict[tuple[int, int], float] = {}
    for i1, box1 in enumerate(box_list):
        for i2, box2 in enumerate(box_list):
            if i1 >= i2:
                continue
            distances[(i1, i2)] = math.dist(box1, box2)
    connections = [i for i, _ in sorted(distances.items(), key=lambda d: d[1])]

    circuits = {}
    for i, (node1, node2) in enumerate(connections):
        update_networks(circuits, (node1, node2))
        if i == NUM_CONNECTIONS - 1:
            part1 = math.prod(
                len(nw) for nw in sorted(circuits.values(), key=lambda c: -len(c))[:3]
            )
        if len(circuits) == 1 and len(next(iter(circuits.values()))) == len(box_list):
            part2 = box_list[node1][0] * box_list[node2][0]
            break

    return part1, part2


# Initially used for part 1, super confusing
def find_networks(connections):
    node_root = {}

    def find_root(node):
        if node_root.setdefault(node, node) != node:
            node_root[node] = find_root(node_root[node])
        return node_root[node]

    for node1, node2 in connections:
        node_root[find_root(node1)] = find_root(node2)

    networks = {}
    for node in node_root:
        root = find_root(node)
        networks.setdefault(root, []).append(node)

    return list(networks.values())
