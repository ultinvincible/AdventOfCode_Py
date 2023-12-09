import copy


def run(input_data: str):
    segments = input_data.split('\n\n')
    seeds = [int(seed) for seed in segments.pop(0)[7:].split()]
    almanac = [[[int(num) for num in line.split()] for line in seg.splitlines()[1:]] for seg in segments]
    for c, conv in enumerate(almanac):
        min_value = float('inf')
        max_value = float('-inf')
        for r, conv_range in enumerate(conv):
            almanac[c][r] = [conv_range[1], conv_range[1] + conv_range[2] - 1, conv_range[0] - conv_range[1]]
            min_value = min((min_value, almanac[c][r][0]))
            max_value = max((max_value, almanac[c][r][1]))
        almanac[c].append([float('-inf'), min_value - 1, 0])
        almanac[c].append([max_value + 1, float('inf'), 0])
    # source min, source max, conversion
    locations = copy.deepcopy(seeds)
    for conversion in almanac:
        for i, value in enumerate(locations):
            for conv_range in conversion[:-2]:
                if conv_range[0] <= value <= conv_range[1]:
                    locations[i] += conv_range[2]
                    break
    part1 = min(locations)

    ranges = []
    for i in range(len(seeds))[::2]:
        ranges.append((seeds[i], seeds[i] + seeds[i + 1] - 1))
    for conversion in almanac:
        new_ranges = []
        for i, value_range in enumerate(ranges):
            for conv_range in conversion:
                start = max((value_range[0], conv_range[0]))
                end = min((value_range[1], conv_range[1]))
                if start > end:
                    continue
                new_ranges.append((start + conv_range[2], end + conv_range[2]))
        ranges = copy.deepcopy(new_ranges)
    part2 = min(ranges, key=lambda r: r[0])[0]
    return part1, part2
