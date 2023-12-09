def run(input_data: str):
    part1 = 0
    part2 = 0
    numbers = []
    symbols = []
    for row, line in enumerate(input_data.splitlines()):
        numbers.append([])
        start = len(line)
        for col, char in enumerate(line):
            if char.isdecimal():
                if start == len(line):
                    start = col
                if start != len(line) and (col == len(line) - 1 or not line[col + 1].isdecimal()):
                    numbers[-1].append((start, col, int(line[start:col + 1])))
                    start = len(line)
            elif char != '.':
                symbols.append((row, col, char))

    parts = set()
    for srow, scol, char in symbols:
        adjacent = []
        for row in range(srow - 1, srow + 2):
            for start, end, value in numbers[row]:
                if start - 1 <= scol:
                    if scol <= end + 1:
                        adjacent.append((row, start, end, value))
                else:
                    break
        for part in adjacent:
            parts.add(part)
        if char == '*' and len(adjacent) == 2:
            part2 += adjacent[0][3] * adjacent[1][3]

    for part in parts:
        part1 += part[3]
    return part1, part2
