from helper import directions_2d, dijkstra


def run(input_data: str):
    city_map = [[int(char) for char in list(line)] for line in input_data.splitlines()]
    lengths = [len(city_map), len(city_map[0])]

    def next_states(
        state: tuple[tuple[int, int], tuple[int, int]],
        max_straight: int,
        min_straight: int,
    ):
        (row, col), from_drt = state
        drts_2d = directions_2d()
        if from_drt:
            for drt in (from_drt, (-from_drt[0], -from_drt[1])):
                try:
                    drts_2d.remove(drt)
                except ValueError:
                    pass
        result: list[tuple[int, tuple[tuple[int, int], tuple[int, int]]]] = []
        for drt_nei in drts_2d:
            i = 0 if drt_nei[0] != 0 else 1
            cost = 0
            for move in range(1, max_straight + 1):
                new_point = [row, col]
                new_point[i] += drt_nei[i] * move
                if not 0 <= new_point[i] < lengths[i]:
                    break
                cost += city_map[new_point[0]][new_point[1]]
                if move >= min_straight:
                    result.append((cost, (tuple(new_point), drt_nei)))

        return result

    parts = []
    for max_straight, min_straight in [(3, 1), (10, 4)]:
        min_cost, _ = dijkstra(
            ((0, 0), None),
            lambda state: next_states(state, max_straight, min_straight),
            lambda state: state[0] == (lengths[0] - 1, lengths[1] - 1),
        )
        parts.append(min_cost)

    return tuple(parts)
