from functools import cache
from typing import Callable

from helper import neighbors_2d


def run(input_data: str):
    input_grid = [list(line) for line in input_data.splitlines()]
    destination = len(input_grid) - 1, len(input_grid[-1]) - 2

    @cache
    def get_neighbors(point: tuple[int, int], climb=False):
        neighbors = [
            (r, c)
            for r, c in neighbors_2d(point, (len(input_grid), len(input_grid[0])))
            if input_grid[r][c] != "#"
        ]

        paths: list[tuple[int, tuple[int, int]]] = []
        for nei in neighbors:
            prev = point
            count = 1
            while True:
                row, col = nei
                if climb or input_grid[row][col] == ".":
                    neighbors = [
                        (r, c)
                        for r, c in neighbors_2d(
                            (row, col), (len(input_grid), len(input_grid[0]))
                        )
                        if (r, c) != prev and input_grid[r][c] != "#"
                    ]
                else:
                    match input_grid[row][col]:
                        case ">":
                            neighbors = [(row, col + 1)]
                        case "v":
                            neighbors = [(row + 1, col)]
                        case "<":
                            neighbors = [(row, col - 1)]
                        case "^":
                            neighbors = [(row - 1, col)]
                        case _:
                            raise Exception
                if len(neighbors) != 1 and neighbors != [point]:
                    paths.append((count, nei))
                    break
                prev = nei
                nei = neighbors[0]
                count += 1
        return paths

    # with open("output.txt", "w") as file:
    #     for point in [(0, 1), (5, 3), (3, 11)]:
    #         for path in next_paths(point):
    #             print(path, file=file)
    #         print(file=file)
    #         for path in next_paths(point, True):
    #             print(path, file=file)
    #         print(file=file)

    before_dest_cost, before_dest = get_neighbors(destination, True)[0]
    hiking_trails = df_search((0, 1), get_neighbors, before_dest)
    path_length = [sum(path.values()) for path in hiking_trails]
    hiking_trails2 = df_search(
        (0, 1), lambda point: get_neighbors(point, True), before_dest
    )
    # hiking_trails2 = []
    path_length2 = [sum(path.values()) for path in hiking_trails2]

    with open("output.txt", "w") as file:
        for path, length in zip(hiking_trails, path_length):
            print(path, file=file)
            print(length, file=file)
        print("-" * 100, file=file)
        for path, length in zip(hiking_trails2, path_length2):
            print(path, file=file)
            print(length, file=file)

    return tuple(
        max(lengths) + before_dest_cost for lengths in (path_length, path_length2)
    )


def df_search[
    Key
](start: Key, get_neighbors: Callable[[Key], list[tuple[int, Key]]], destination: Key):
    def extend(node: Key, path: dict[Key, int] = None):
        if path is None:
            path = {node: 0}
        neighbors: list[tuple[int, Key]] = [
            (cost, nei) for cost, nei in get_neighbors(node) if nei not in path
        ]

        if node != destination:
            if not neighbors:
                return []
        else:
            return [path.copy()]

        result = []
        for cost, nei in neighbors:
            path[nei] = cost
            result.extend(extend(nei, path))
            path.pop(nei)
        return result

    return extend(start)
