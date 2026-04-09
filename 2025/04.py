from helper import neighbors_2d


def run(input_data: str):
    part1, part2 = 0, 0

    input_grid = [list(line) for line in input_data.splitlines()]
    part1, input_grid = remove_rolls(input_grid)

    part2 = part1
    while True:
        count_remove, input_grid = remove_rolls(input_grid)
        if count_remove == 0:
            break
        part2 += count_remove

    return part1, part2


def remove_rolls(input_grid):
    new_grid = [list(row) for row in input_grid]
    count_remove = 0
    for row, line in enumerate(input_grid):
        for col, point in enumerate(line):
            if point != "@":
                continue
            count_rolls = 0
            for nei_row, nei_col in neighbors_2d(
                (row, col), (len(input_grid), len(line)), True
            ):
                if input_grid[nei_row][nei_col] == "@":
                    count_rolls += 1
            if count_rolls < 4:
                new_grid[row][col] = "."
                count_remove += 1

    return count_remove, new_grid
