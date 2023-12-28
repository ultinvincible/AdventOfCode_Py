from helper import dijkstra, neighbors_2d


def run(input_data: str):
    city_map = [[int(i) for i in list(s)] for s in input_data.splitlines()]
    col_row_view = list(zip(*city_map))
    lengths = [len(city_map), len(city_map[0])]
    (max_straight, min_straight) = (1, 1)

    def next_states(state):
        (point, drt, consecutive) = state
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

    # def get_node(state):
    #     try:
    #         return state_map[state[0][0]][state[0][1]][tuple(state[1:])]
    #     except KeyError:
    #         return (None, float("inf"), False)

    # def set_node(state, node):
    #     state_map[state[0][0]][state[0][1]][tuple(state[1:])] = node

    parts = []
    for max_straight, min_straight in [(3, 1), (10, 4)]:
        # state_map = [[{} for _ in city_map[0]] for _ in city_map]
        state_tree = dijkstra(next_states, ((0, 0), None, 0))
        end_states = [
            ((point, _, cons), cost)
            for (point, _, cons), (_, cost, _) in state_tree.items()
            if point == (lengths[0] - 1, lengths[1] - 1) and cons >= min_straight
        ]
        costs = [state[1] for state in end_states]
        i = costs.index(min(costs))
        parts.append(costs[i])

        # state = end_states[i][0]
        # # path = []
        # while state is not None:
        #     # path.append(state)
        #     print(f"{state}\t{state_tree[state][1]}")
        #     state = state_tree[state][0]
        # # for row, line in enumerate(city_map):
        # #     for col, point in enumerate(line):
        # #         if (row, col) in path:
        # #             print(".", end="")
        # #         else:
        # #             print(point, end="")
        # #     print()

    return tuple(parts)
