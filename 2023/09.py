def run(input_data: str):
    part1 = 0
    part2 = 0
    for _, line in enumerate(input_data.splitlines()):
        sequences = [[int(value) for value in line.split()]]
        while not sequences[-1].count(sequences[-1][0]) == len(sequences[-1]):
            sequences.append([])
            for i in range(len(sequences[-2]) - 1):
                sequences[-1].append(sequences[-2][i + 1] - sequences[-2][i])
        part1 += sum([sequence[-1] for sequence in sequences])
        prev = 0
        for sequence in sequences[::-1]:
            prev = sequence[0] - prev
        part2 += prev

    return part1, part2
