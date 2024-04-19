from helper import neighbors_2d, dijkstra


def run(input_data: str):
    city_map = [[int(i) for i in list(s)] for s in input_data.splitlines()]
    col_row_view = list(zip(*city_map))
    lengths = [len(city_map), len(city_map[0])]

    def next_states(state, max_straight: int, min_straight: int):
        point, drt, consecutive = state
        neis = neighbors_2d(point, lengths)
        if drt is not None:
            neis.pop((-drt[0], -drt[1]))
        if consecutive == max_straight:
            neis.pop(drt, None)
        result = []
        for drt_nei, (nei_row, nei_col) in neis.items():
            if drt_nei == drt:
                result.append(
                    (
                        city_map[nei_row][nei_col],
                        ((nei_row, nei_col), drt_nei, consecutive + 1),
                    )
                )
            else:
                i = 0 if drt_nei[0] != 0 else 1
                new_point = list(point)
                new_point[i] += drt_nei[i] * min_straight
                if 0 <= new_point[i] < lengths[i]:
                    range_max = new_point[i] + drt_nei[i]
                    if range_max == -1:
                        range_max = None
                    cost = sum(
                        city_map[point[0]][nei_col : range_max : drt_nei[i]]
                        if i == 1
                        else col_row_view[point[1]][nei_row : range_max : drt_nei[i]]
                    )
                    result.append((cost, (tuple(new_point), drt_nei, min_straight)))

        return result

    parts = []
    for max_straight, min_straight in [(3, 1), (10, 4)]:
        min_cost, _ = dijkstra(
            ((0, 0), None, 0),
            lambda state: next_states(state, max_straight, min_straight),
            lambda state: state[0] == (lengths[0] - 1, lengths[1] - 1),
        )
        parts.append(min_cost)

    return tuple(parts)
