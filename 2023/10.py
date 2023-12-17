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

    return part1, part2
