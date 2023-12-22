def run(input_data: str):
    part1 = 0
    part2 = 0
    for _, input_map in enumerate(input_data.split("\n\n")):
        mirror_map = input_map.splitlines()
        rows = [list(s) for s in mirror_map]
        cols = [[row[c] for row in mirror_map] for c in range(len(mirror_map[0]))]
        mirrors = find_mirror(rows, 100)
        if len(mirrors) < 2:
            mirrors.extend(find_mirror(cols))
        for m, diff in mirrors:
            if diff == 0:
                part1 += m
            elif diff == 1:
                part2 += m

    return part1, part2


def find_mirror(mirror_map, multiplier=1):
    result = []
    for i in range(1, len(mirror_map)):
        diff = 0
        for r1, r2 in zip(mirror_map[i - 1 :: -1], mirror_map[i:]):
            for p1, p2 in zip(r1, r2):
                if p1 != p2:
                    diff += 1
                if diff > 1:
                    break
            if diff > 1:
                break
        if diff <= 1:
            result.append((i * multiplier, diff))
    return result
