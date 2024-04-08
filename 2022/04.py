def run(input_data: str):
    part1 = 0
    part2 = 0

    pairs = [
        tuple(int(value) for value in line.replace(",", "-").split("-"))
        for line in input_data.splitlines()
    ]
    for start1, end1, start2, end2 in pairs:
        if (start1 - start2) * (end1 - end2) <= 0:
            part1 += 1
    for start1, end1, start2, end2 in pairs:
        if end1 >= start2 and end2 >= start1:
            part2 += 1
    return part1, part2
