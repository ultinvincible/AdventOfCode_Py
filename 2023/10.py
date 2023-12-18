import math


def run(input_data: str):
    part2 = 0
    symbols = "|-LJ7F"
    pipe_types = [(1, 3), (0, 2), (0, 1), (1, 2), (2, 3), (0, 3)]
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    pipe_map = []
    for r, row in enumerate(input_data.splitlines()):
        pipe_map.append({})
        for c, pipe in enumerate(row):
            match pipe:
                case "S":
                    start = (r, c)
                case ".":
                    pass
                case _:
                    pipe_map[-1][c] = pipe_types[symbols.index(pipe)]

    loop = [start]
    old_d = 0
    start_pipe = []
    for d, (r, c) in enumerate(directions):
        if (
            0 <= start[0] + r < len(pipe_map)
            and start[1] + c in pipe_map[start[0] + r]
            and (d + 2) % 4 in pipe_map[start[0] + r][start[1] + c]
        ):
            if len(loop) == 1:
                loop.append((start[0] + r, start[1] + c))
                old_d = d
            else:
                loop.insert(0, (start[0] + r, start[1] + c))
            start_pipe.append(d)
    pipe_map[start[0]][start[1]] = tuple(start_pipe)

    while loop[-1] != loop[0]:
        row, col = loop[-1]
        pipe = pipe_map[row][col]
        d = pipe[0] if pipe[0] != (old_d + 2) % 4 else pipe[1]
        (r, c) = directions[d]
        if 0 <= row + r < len(pipe_map) and col + c in pipe_map[row + r]:
            loop.append((row + r, col + c))
            old_d = d
    loop.pop()
    part1 = math.floor(len(loop) / 2)

    loop.sort()
    enclosed = []
    (prev_row, prev_col) = (-1, -1)
    prev_drt = 0
    inside = False
    for row, col in loop:
        if row != prev_row:
            inside = False
        if inside and col - prev_col > 1:
            enclosed.append((row, prev_col + 1, col))

        pipe = pipe_map[row][col]
        match pipe:
            case (1, 3):
                inside = not inside
            case (0, 1) | (0, 3):
                prev_drt = pipe[1]
            case (1, 2) | (2, 3):
                drt = 1 if pipe[0] != 2 else 3
                if drt != prev_drt:
                    inside = not inside
        (prev_row, prev_col) = (row, col)

    # test = [list(s) for s in input_data.splitlines()]
    # for row, col1, col2 in enclosed:
    #     for col in range(col1, col2):
    #         test[row][col] = "\u2588"
    # for line in test:
    #     print("".join(line))
    # print([r for r in enclosed if r[1] + 1 != r[2]])
    part2 = sum(r[2] - r[1] for r in enclosed)

    return part1, part2
