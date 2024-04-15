import heapq
from typing import Callable, Hashable

directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def neighbors_2d(
    point: tuple[int, int], bounds: tuple[int, int], diagonal=False
) -> dict[tuple[int, int], tuple[int, int]]:
    """On a 2D square grid/table/matrix, generates neighbors for a point.

    Args:
        point: The 2D point, represented by tuple(row,col)
        bounds: Higher bounds for row and col
        diagonal: Include diagonal neighbors, defaults to False

    Returns:
        dict[tuple[int, int], tuple[int, int]]: Mapping of directions to neighbors.
    """
    row, col = point
    neis = {}
    for r, c in directions if not diagonal else directions + diagonals:
        nei = row + r, col + c
        # Reminder that try except IndexError doesnt work because negative indices are allowed.
        if all(0 <= nei[i] < bounds[i] for i in (0, 1)):
            neis[r, c] = nei
    return neis


def dijkstra(
    get_neighbors: Callable[[Hashable], list[tuple[Hashable, int]]],
    start: Hashable,
    is_destination: None | Callable[[Hashable], bool] = None,
    get_set_node: (
        tuple[
            Callable[[Hashable], tuple[Hashable, int, bool]],
            Callable[[Hashable, tuple[Hashable, int, bool]], None],
        ]
        | None
    ) = None,
) -> dict[Hashable, tuple[Hashable, int, bool]] | None:
    """A dynamic implementation of Dijkstra's algorithm, supporting infinite graphs (uniform cost search) and manages nodes using keys.

    Stores nodes in a dict by default. Each node is represented by a tuple: (
        Key of the previous node in the minimum cost path: Hashable,
        The current minimum cost: int,
        Whether the node has been visited: bool
    )

    Args:
        get_neighbors: Function to find all neighbors of the node with the given key
        start: Key of the starting node
        is_destination: Function to check if the algorithm should end at the current node
        get_set_node: Tuple of functions to get and set node value from key

    Returns:
        Dict of keys to nodes if get_set_node is not specified, else None.
    """

    if get_set_node:
        get_node, set_node = get_set_node
    else:
        nodes_dict: dict[Hashable, tuple[Hashable, int, bool]] = {}

        get_node, set_node = (
            lambda key: nodes_dict.get(key, (None, float("inf"), False)),
            lambda key, node: nodes_dict.update([(key, node)]),
        )

    current = start
    set_node(start, (None, 0, False))
    priority_queue = [(0, start)]

    while not (is_destination and is_destination(current)) and priority_queue:
        _, current = heapq.heappop(priority_queue)
        prev, current_cost, visited = get_node(current)
        if visited:
            continue

        for nei, cost in get_neighbors(current):
            _, nei_cost, nei_visited = get_node(nei)

            # A* would skip this check, but the heuristic has to be good enough:
            if nei_visited:
                continue

            # A* heuristic would be added here:
            new_cost = current_cost + cost  # + h(nei)
            if new_cost < nei_cost:
                set_node(nei, (current, new_cost, False))
                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        nei,
                    ),
                )

        set_node(current, (prev, current_cost, True))

    if get_set_node is None:
        return nodes_dict
