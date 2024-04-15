import helper


def run(input_data: str):
    height_map = input_data.splitlines()

    for row, line in enumerate(height_map):
        if (col := line.find("S")) != -1:
            start_row, start_col = row, col

        if (col := line.find("E")) != -1:
            end_row, end_col = row, col

    return (
        bf_search_steps(height_map, start_row, start_col),
        bf_search_steps(height_map, end_row, end_col, True),
    )


def bf_search_steps(
    height_map: list[str], start_row: int, start_col: int, reverse=False
):
    BFS_queue = [(start_row, start_col, 0)]
    explored = [[False for _ in line] for line in height_map]
    explored[start_row][start_col] = True

    result = 0
    while BFS_queue and not result:
        row, col, steps = BFS_queue.pop(0)

        square = (
            height_map[row][col]
            if (row, col) != (start_row, start_col)
            else ("a" if not reverse else "z")
        )
        neis = helper.neighbors_2d(
            (row, col), (len(height_map), len(height_map[0]))
        ).values()

        for nei_row, nei_col in neis:
            nei = height_map[nei_row][nei_col]
            if (
                ord(nei) > ord(square) + 1
                if not reverse
                else ord(nei) < ord(square) - 1
            ):
                continue

            if nei == ("E" if not reverse else "a"):
                result = steps + 1
                break

            if not explored[nei_row][nei_col]:
                explored[nei_row][nei_col] = True
                BFS_queue.append((nei_row, nei_col, steps + 1))

    # print("\n".join("".join("#" if e else "." for e in line) for line in explored))
    return result
