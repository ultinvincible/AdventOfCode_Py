def priority(char):
    return (
        ord(char) - ord("A") + 27 if ord(char) < ord("a") else ord(char) - ord("a") + 1
    )


def run(input_data: str):
    part1 = 0
    part2 = 0

    rucksacks = input_data.splitlines()
    for rs in rucksacks:
        for item in rs[: len(rs) // 2]:
            if item in rs[len(rs) // 2 :]:
                part1 += priority(item)
                break
    for r in range(0, len(rucksacks), 3):
        for item in rucksacks[r]:
            if item in rucksacks[r + 1] and item in rucksacks[r + 2]:
                part2 += priority(item)
                break
    return part1, part2
