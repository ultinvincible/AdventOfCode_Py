def get_max_joltages(rank: list[int], num_battery=2):
    max_joltages = []
    search_start = 0
    search_end = len(rank) + 1 - num_battery
    while len(max_joltages) < num_battery:
        search = rank[search_start:search_end]
        max_joltage = max(search)
        max_joltages.append(max_joltage)
        search_start += search.index(max_joltage) + 1
        search_end += 1

    return max_joltages


def run(input_data: str):
    part1, part2 = 0, 0

    input_grid = [list(line) for line in input_data.splitlines()]
    for _, line in enumerate(input_grid):
        rank = list(map(int, line))
        max_joltages = get_max_joltages(rank)
        part1 += sum(joltage * 10**i for i, joltage in enumerate(max_joltages[::-1]))
        max_joltages = get_max_joltages(rank, 12)
        part2 += sum(joltage * 10**i for i, joltage in enumerate(max_joltages[::-1]))

    return part1, part2
