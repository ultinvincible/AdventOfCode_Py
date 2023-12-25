import bisect
from collections import Counter


def run(input_data: str):
    # for col in zip(*rock_map):
    #     rounds_cube = [[0, 0]]
    #     for r, rock in enumerate(col):
    #         match rock:
    #             case "O":
    #                 rounds_cube[-1][0] += 1
    #             case "#":
    #                 rounds_cube.append([0, r + 1])
    #     weight = 0
    #     for rc in rounds_cube:
    #         rounds, cube = tuple(rc)
    #         weight += int((lengths[0] - cube - (rounds - 1) / 2) * rounds)
    #     part1 += weight

    part1 = 0
    part2 = 0
    rock_map = input_data.splitlines()
    lengths = [len(rock_map), len(rock_map[0])]
    rounds_histories = [[]]
    cubes = [[[] for _ in rock_map], [[] for _ in rock_map[0]]]
    for row, line in enumerate(rock_map):
        for col, rock in enumerate(line):
            if rock == "O":
                rounds_histories[0].append((row, col))
            elif rock == "#":
                cubes[0][row].append(col)
                cubes[1][col].append(row)
    directions = [(1, -1), (0, -1), (1, 1), (0, 1)]

    r = 0
    # repeat = [(0, 0) for _ in rounds_histories[0]]
    for _ in range(1000000000):
        rounds_prev = list(rounds_histories[-1])
        for drt in directions:
            rounds_current = []
            for round_rock in rounds_prev:
                new_rock = list(round_rock)
                line = cubes[drt[0]][new_rock[drt[0]]]
                i = bisect.bisect_left(line, new_rock[1 - drt[0]]) + (
                    0 if drt[1] == 1 else -1
                )
                if i in (-1, len(line)):
                    move = -1 if i == -1 else lengths[1 - drt[0]]
                else:
                    move = line[i]
                new_rock[1 - drt[0]] = move - drt[1]
                while tuple(new_rock) in rounds_current:
                    new_rock[1 - drt[0]] -= drt[1]
                rounds_current.append(tuple(new_rock))
            if len(rounds_histories) == 1 and drt == (1, -1):
                part1 = sum(lengths[0] - round[0] for round in rounds_current)
            rounds_prev = rounds_current

        # print(rounds_current)
        # for row, line in enumerate(rock_map):
        #     line = list(line)
        #     for col, rock in enumerate(line):
        #         char = rock
        #         if (row, col) in rounds_current:
        #             char = "O"
        #         elif char == "O":
        #             char = "."
        #         print(char, end="")
        #     print()
        # print()

        matches = [(r, h) for (r, h) in enumerate(rounds_histories) if Counter(h) == Counter(rounds_current)]
        if len(matches)==1:
            r=matches[0][0]
            (start, step) = (r, len(rounds_histories) - r)
            break
        rounds_histories.append(list(rounds_current))

    cycle = 1000000000 % step
    if cycle < start:
        cycle += step
    part2 = sum(lengths[0] - round[0] for round in rounds_histories[cycle])

    return part1, part2
