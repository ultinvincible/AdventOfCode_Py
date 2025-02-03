from helper import neighbors_2d


def run(input_data: str):
    part2 = 0

    input_grid = input_data.splitlines()
    for row, line in enumerate(input_grid):
        if (start_col := line.find("S")) != -1:
            start = row, start_col
            break
    reach = [[start]]
    for step in range(1, 65):
        next_reach = set()
        for point in reach[-1]:
            next_reach.update(
                (row, col)
                for row, col in neighbors_2d(
                    point, (len(input_grid), len(input_grid[0]))
                )
                if input_grid[row][col] != "#"
            )
        reach.append(list(next_reach))

    step_grid = [list(line) for line in input_grid]
    for step, step_reach in enumerate(reach):
        for row, col in step_reach:
            step_grid[row][col] = str(step)[-1]
    with open("output.txt", "w") as file:
        # print(
        #     "\n".join(
        #         f"{step:02}| {step_reach}" for step, step_reach in enumerate(reach)
        #     ),
        #     file=file,
        # )
        print(
            "\n".join("".join(line) for line in step_grid),
            file=file,
        )

    return len(reach[-1]), part2
