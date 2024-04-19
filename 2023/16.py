from functools import cache
from helper import directions_2d


def behavior(drt, tile):
    (row, col) = drt
    match tile:
        case "/":
            return [(-col, -row)]
        case "\\":
            return [(col, row)]
        case "|":
            if row == 0:
                return [(-1, 0), (1, 0)]
        case "-":
            if col == 0:
                return [(0, -1), (0, 1)]
    return [drt]


def run(input_data: str):
    part1 = 0
    part2 = 0
    light_map = [list(s) for s in input_data.splitlines()]
    lengths = (len(light_map), len(light_map[0]))
    starts = []
    for drt in directions_2d():
        dim = 0 if drt[0] == 0 else 1
        for i in range(lengths[dim]):
            start = [0, 0]
            start[dim] = i
            start[1 - dim] = -1 if drt[1 - dim] == 1 else lengths[1 - dim]
            starts.append([(tuple(start), drt)])

    @cache
    def run_line(row, col, drt):
        energized = set()
        (new_row, new_col) = (row, col)
        new_drt_list = [drt]
        while new_drt_list == [drt]:
            (new_row, new_col) = (new_row + drt[0], new_col + drt[1])
            if any(not 0 <= (new_row, new_col)[i] < lengths[i] for i in (0, 1)):
                new_drt_list = []
            else:
                new_drt_list = behavior(drt, light_map[new_row][new_col])
                energized.add((new_row, new_col))
        return new_row, new_col, new_drt_list, energized

    beams: list[tuple[int, int]]
    for beams in starts:
        current_i = 0
        energized = set()
        while current_i < len(beams):
            (row, col), drt = beams[current_i]
            new_row, new_col, new_drt_list, new_energized = run_line(row, col, drt)
            for new_drt in new_drt_list:
                if ((new_row, new_col), new_drt) not in beams:
                    beams.append(((new_row, new_col), new_drt))
            energized = energized.union(new_energized)
            current_i += 1

        if beams[0] == ((0, -1), (0, 1)):
            part1 = len(energized)
        part2 = max(part2, len(energized))

    return part1, part2
