def run(input_data: str):
    part1, part2 = 0, 0

    dial_pos = 50
    for line in input_data.splitlines():
        value = int(line[1:])
        if line[0] == "L":
            value *= -1

        new_dial_pos = dial_pos + value

        if new_dial_pos > 0:
            zeroes = new_dial_pos // 100
        else:
            zeroes = -(new_dial_pos) // 100 + 1
            if dial_pos == 0:
                zeroes -= 1
        part2 += zeroes

        dial_pos = new_dial_pos % 100
        if dial_pos == 0:
            part1 += 1

    return part1, part2
