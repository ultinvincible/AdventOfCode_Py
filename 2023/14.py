from functools import cache


@cache
def move_line(line: str):
    new_line: list[str] = list(line)
    dest_i = 0
    for line_i, char in enumerate(line):
        match char:
            case "#":
                dest_i = line_i + 1
            case "O":
                if line_i != dest_i:
                    new_line[dest_i] = "O"
                    new_line[line_i] = "."
                dest_i += 1
    return "".join(new_line)


def run(input_data: str):
    part1, part2 = 0, 0
    rock_map = [list(line) for line in input_data.splitlines()]
    for col in zip(*rock_map):
        stacks = [[0, 0]]
        for row, rock in enumerate(col):
            match rock:
                case "O":
                    stacks[-1][0] += 1
                case "#":
                    stacks.append([0, row + 1])
        load = sum(
            (len(rock_map) - row) * count - (count - 1) * count // 2
            for count, row in stacks
        )
        part1 += load

    rock_map = list(zip(*rock_map))
    map_history = {to_tuple(rock_map): 0}
    output = ["\n".join(to_tuple(rock_map))]
    for cycle in range(10**9):
        output.append("Cycle " + str(cycle))
        for _ in range(4):
            rock_map = [move_line(line) for line in rock_map]
            # rotate counter-clockwise
            rock_map = list(zip(*(line[::-1] for line in rock_map)))
            if len(rock_map) <= 10:
                output.append("\n".join(to_tuple(rock_map)) + "\n")

        map_str = to_tuple(rock_map)
        load = map_load(list(zip(*rock_map)))
        output.append(load)
        if repeated_cycle := map_history.get(map_str, None):
            dest_cycle = repeated_cycle + (10**9 - cycle - 1) % (
                cycle + 1 - repeated_cycle
            )
            dest_map = [
                _map for _map, cycle in map_history.items() if cycle == dest_cycle
            ][0]
            dest_map = list(zip(*dest_map))
            output.append((cycle, repeated_cycle, dest_cycle))
            break
        map_history[map_str] = cycle + 1

    part2 = map_load(dest_map)
    with open("output.txt", "w") as file:
        [print(line, file=file) for line in output]
    return part1, part2


def map_load(rock_map):
    return sum(
        len(rock_map) - row
        for row, line in enumerate(rock_map)
        for rock in line
        if rock == "O"
    )


def to_tuple(rock_map: tuple[str]):
    return tuple("".join(line) for line in rock_map)
