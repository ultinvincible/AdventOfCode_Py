from helper import dijkstra, neighbors_2d


def run(input_data: str):
    city_map = [[int(i) for i in list(s)] for s in input_data.splitlines()]
    col_row_view = list(zip(*city_map))
    lengths = [len(city_map), len(city_map[0])]
    max_straight, min_straight = 1, 1

    def next_states(state):
        point, drt, consecutive = state
        neis = neighbors_2d(point, lengths)
        if drt is not None:
            neis.pop((-drt[0], -drt[1]))
        if consecutive == max_straight:
            try:
                neis.pop(drt)
            except KeyError:
                pass
        result = []
        for d, p in neis.items():
            if d == drt:
                result.append(((p, d, consecutive + 1), city_map[p[0]][p[1]]))
            else:
                i = 0 if d[0] != 0 else 1
                new_point = list(point)
                new_point[i] += d[i] * min_straight
                if 0 <= new_point[i] < lengths[i]:
                    range_max = new_point[i] + d[i]
                    if range_max == -1:
                        range_max = None
                    cost = sum(
                        city_map[point[0]][p[1] : range_max : d[i]]
                        if i == 1
                        else col_row_view[point[1]][p[0] : range_max : d[i]]
                    )
                    result.append(((tuple(new_point), d, min_straight), cost))

        return result

    parts = []
    for max_straight, min_straight in [(3, 1), (10, 4)]:
        state_tree = dijkstra(next_states, ((0, 0), None, 0))
        end_states = [
            ((point, drt, cons), cost)
            for (point, drt, cons), (_, cost, _) in state_tree.items()
            if point == (lengths[0] - 1, lengths[1] - 1)
        ]
        costs = [state[1] for state in end_states]
        parts.append(min(costs))

        # with open("output", "w") as file:
        #     if max_straight == 3:
        #         continue

        #     # print(end_states)
        #     state = end_states[costs.index(min(costs))][0]
        #     while state is not None:
        #         prev_state = state_tree[state]
        #         print(f"{str(state):30}\t{prev_state[1]}", file=file)
        #         state = prev_state[0]

    return tuple(parts)
