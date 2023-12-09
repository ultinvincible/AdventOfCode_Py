from typing import *


def dijkstra(get_neighbors: Callable[[Any], List[tuple[Any, int]]], start, is_destination=None):
    visited: dict[Any, tuple[Any, int]] = {}
    unvisited: dict[Any, tuple[Any, int]] = {}
    current = start

    while True:
        for nei, cost in get_neighbors(current):
            new_cost = unvisited[current][1] + cost
            if nei not in visited.keys() and nei not in unvisited.keys():
                unvisited[nei] = (current, new_cost)

        visited[current] = unvisited[current]
        unvisited.pop(current)

        if is_destination is not None and is_destination(current) or len(unvisited) == 0:
            break

        min_cost = pow(2, 30)
        for state, (_, cost) in unvisited:
            if min_cost > cost:
                current = state
                min_cost = cost

    return visited
