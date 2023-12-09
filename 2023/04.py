import re


def run(input_data: str):
    part1 = 0
    splitlines = input_data.splitlines()
    copies = [1 for i in range(len(splitlines))]
    for i, line in enumerate(splitlines):
        lists = [str.split(split) for split in re.split('[:|]', line)][1:]
        matches = 0
        for win in lists[0]:
            for have in lists[1]:
                if win == have:
                    matches += 1
        part1 += int(pow(2, matches - 1)) if matches > 0 else 0

        for j in range(matches):
            if i + j + 1 < len(copies):
                copies[i + j + 1] += copies[i]
    part2 = sum(copies)

    return part1, part2
