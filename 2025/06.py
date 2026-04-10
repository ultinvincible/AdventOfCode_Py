import math


def run(input_data: str):
    part1, part2 = 0, 0

    input_grid = [line.split() for line in input_data.splitlines()]
    num_rows = len(input_grid) - 1
    for col, op in enumerate(input_grid[-1]):
        func = sum if op == "+" else math.prod
        part1 += func(int(input_grid[row][col]) for row in range(num_rows))

    input_grid = [list(line) for line in input_data.splitlines()]
    nums = []
    func = None
    for col, op in enumerate(input_grid[-1]):
        if col == len(input_grid[0]) - 1 or input_grid[-1][col + 1] == " ":
            func = sum if op == "+" else math.prod if op == "*" else func
            digits = [
                int(input_grid[row][col])
                for row in range(num_rows)
                if input_grid[row][col] != " "
            ]
            nums.append(sum(digit * 10**i for i, digit in enumerate(digits[::-1])))
        if col == len(input_grid[0]) - 1 or input_grid[-1][col + 1] != " ":
            part2 += func(nums)
            nums = []
    return part1, part2
