from typing import Callable, Hashable, NamedTuple
import heapq


def neighbors_2d(point, bounds) -> dict[tuple[int, int], tuple[int, int]]:
    (row, col) = point
    neis = {}
    for r, c in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
        i = 0 if r != 0 else 1
        if 0 <= (row, col)[i] + (r, c)[i] < bounds[i]:
            neis[r, c] = (row + r, col + c)
    return neis


def dijkstra(
    get_neighbors: Callable[[Hashable], list[tuple[Hashable, int]]],
    start,
    get_set_node: None
    | tuple[
        Callable[[Hashable], tuple[Hashable, int, bool]],
        Callable[[Hashable, tuple[Hashable, int, bool]], None],
    ] = None,
    is_destination: None | Callable[[Hashable], bool] = None,
):
    if get_set_node is not None:
        (get_node, set_node) = get_set_node
    else:
        nodes_dict: dict[Hashable, tuple[Hashable, int, bool]] = {}

        def dict_get(key):
            try:
                return nodes_dict[key]
            except KeyError:
                return (None, float("inf"), False)

        def dict_set(key, value):
            nodes_dict[key] = value

        (get_node, set_node) = (dict_get, dict_set)

    current = start
    set_node(start, (None, 0, False))
    to_visit_heap = [(0, start)]

    while (is_destination is None or not is_destination(current)) and len(
        to_visit_heap
    ) != 0:
        cost, current = heapq.heappop(to_visit_heap)
        prev, current_cost, visited = get_node(current)
        if visited or cost > current_cost:
            continue

        for nei, cost in get_neighbors(current):
            nei_node = get_node(nei)
            if nei_node[2]:
                continue
            new_cost = current_cost + cost
            if new_cost < nei_node[1]:
                set_node(nei, (current, new_cost, False))
            heapq.heappush(
                to_visit_heap,
                (
                    min(
                        new_cost, nei_node[1] if nei_node is not None else float("inf")
                    ),
                    nei,
                ),
            )

        set_node(current, (prev, current_cost, True))

    if get_set_node is None:
        return nodes_dict
