import heapq
import math
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
    start: Hashable,
    get_neighbors: Callable[[Hashable], list[tuple[Hashable, int]]],
    is_goal: None | Callable[[Hashable], bool] = None,
) -> dict[Hashable, tuple[Hashable, int]]:
    """A dynamic implementation of Dijkstra's algorithm, supporting infinite graphs (uniform cost search),
    and terminates when no more nodes are found or the is_goal condition is True.

    Nodes are stored as values in a dict, and each node is a tuple containing its:
    - Minimum path cost
    - Parent in the minimum cost tree

    Args:
        start: Key of the starting node
        get_neighbors: Function to find all neighbor nodes of the node with the given key
        is_goal: Function to check if the algorithm should end at the current node, defaults to None

    Returns:
        Dict of keys to nodes
    """
    current_key = start
    # [(cost, key)]:
    frontier = [(int(), start)]
    # {key: (cost, parent_key)} (include expanded and frontier):
    min_path_tree: dict[Hashable, tuple[int, Hashable]] = {}
    is_goal = is_goal or (lambda _: False)

    while frontier and not is_goal(current_key):
        current_cost, current_key = heapq.heappop(frontier)

        for nei_key, nei_cost in get_neighbors(current_key):
            tree_cost, _ = min_path_tree.get(nei_key, (math.inf, None))
            # A* heuristic would be added here:
            new_cost = current_cost + nei_cost  # + h(nei)

            if new_cost < tree_cost:
                min_path_tree[nei_key] = new_cost, current_key
                heapq.heappush(
                    frontier,
                    (
                        new_cost,
                        nei_key,
                    ),
                )

    return min_path_tree
