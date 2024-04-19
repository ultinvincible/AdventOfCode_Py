import heapq
import math
from queue import SimpleQueue
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


def bf_search(
    start: Hashable,
    get_neighbors: Callable[[Hashable], list[Hashable]],
    is_goal: Callable[[Hashable], bool] | None = None,
) -> tuple[dict[Hashable, tuple[int, Hashable]], int]:
    """Best first search, supporting infinite graphs, and stores nodes as values in a dict.
    Each node is mapped to its path length and parent in the path tree.

    Args:
        get_neighbors: Function to find neighbor nodes
        start: The starting node
        is_goal: Function to check if the algorithm should end at the current node, defaults to None

    Returns:
        Dict of nodes to path length and parent nodes/ Path tree, and the path length to reach the last node
    """
    # [(path_length, node)]:
    queue: SimpleQueue[tuple[int, Hashable]] = SimpleQueue()
    explored: set[Hashable] = {start}
    queue.put((0, start))

    # {node: (path_length, parent_node)}:
    path_tree: dict[Hashable, tuple[int, Hashable]] = {start: (0, None)}
    is_goal = is_goal or (lambda _: False)

    while not queue.empty():
        path_length, current_node = queue.get()
        if is_goal(current_node):
            break

        for nei in get_neighbors(current_node):
            if not nei in explored:
                explored.add(nei)
                path_tree[nei] = path_length + 1, current_node
                queue.put((path_length + 1, nei))

    return path_length, path_tree


def dijkstra(
    start: Hashable,
    get_neighbors: Callable[[Hashable], list[tuple[int, Hashable]]],
    is_goal: Callable[[Hashable], bool] | None = None,
) -> tuple[dict[Hashable, tuple[int, Hashable]], int]:
    """A dynamic implementation of Dijkstra's algorithm, supporting infinite graphs (uniform cost search),
    and terminates when no more nodes are found or the is_goal condition is True.

    Nodes are stored as values in a dict; each node contains
    its minimum path cost and key of parent node in the minimum cost tree.

    Args:
        start: Key of the starting node
        get_neighbors: Function to find path costs to and keys of neighbor nodes
        of the node with the given key
        is_goal: Function to check if the algorithm should end at the current node, defaults to None

    Returns:
        Dict of keys to nodes/ Minimum path tree, and the minimum cost to reach the last node
    """
    # [(cost, key)]:
    frontier = [(int(), start)]
    # {key: (cost, parent_key)} (include expanded and frontier):
    min_path_tree: dict[Hashable, tuple[int, Hashable]] = {start: (0, None)}

    is_goal = is_goal or (lambda _: False)

    while frontier:
        current_cost, current_key = heapq.heappop(frontier)
        if is_goal(current_key):
            break

        for nei_cost, nei_key in get_neighbors(current_key):
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

    return current_cost, min_path_tree
