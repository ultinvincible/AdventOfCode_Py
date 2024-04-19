from helper import neighbors_2d, bf_search


def height(char: str):
    match char:
        case "S":
            return ord("a")
        case "E":
            return ord("z")
        case _:
            return ord(char)


def run(input_data: str):
    height_map = input_data.splitlines()

    for row, line in enumerate(height_map):
        if (col := line.find("S")) != -1:
            start = row, col

        if (col := line.find("E")) != -1:
            end = row, col

    def get_neighbors(square: tuple[int, int], reverse=False):
        neis_2d = neighbors_2d(square, (len(height_map), len(height_map[0])))
        for nei in neis_2d.copy():
            square_char, nei_char = tuple(
                height_map[point[0]][point[1]] for point in (square, nei)
            )
            if (
                height(nei_char) > height(square_char) + 1
                if not reverse
                else height(square_char) > height(nei_char) + 1
            ):
                neis_2d.remove(nei)
        return list(neis_2d)

    part1, _ = bf_search(
        start,
        get_neighbors,
        lambda point: height_map[point[0]][point[1]] == "E",
    )
    part2, _ = bf_search(
        end,
        lambda point: get_neighbors(point, True),
        lambda point: height_map[point[0]][point[1]] == "a",
    )
    return part1, part2
