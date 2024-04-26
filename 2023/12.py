def df_search(record: str, groups: tuple[int], index=0) -> list[str]:
    if not groups:
        if "#" in record[index:]:
            return []
        return [record.replace("?", ".")]
    index = (
        [index + i for i, spring in enumerate(record[index:]) if spring != "."]
        or [len(record)]
    )[0]
    if index + sum(groups) + len(groups) - 2 >= len(record):
        return []

    group_length = groups[0]
    end_i = index + group_length
    arrangements: list[tuple[str, tuple[int], int]] = []

    if (
        end_i <= len(record)
        and (index == 0 or record[index - 1] != "#")
        and not "." in record[index:end_i]
        and (end_i == len(record) or record[end_i] != "#")
    ):
        new_record = list(record)
        if index >= 1:
            new_record[index - 1] = "."
        new_record[index:end_i] = ["#"] * group_length
        if end_i < len(record):
            new_record[end_i] = "."
        arrangements.append(("".join(new_record), groups[1:], end_i + 1))

    if record[index] == "?":
        new_record = list(record)
        new_record[index] = "."
        arrangements.append(("".join(new_record), groups, index + 1))

    result: list[str] = []
    for new_arrangement, new_groups, new_index in arrangements:
        result.extend(df_search(new_arrangement, new_groups, new_index))

    return result


def find_combinations(record: str, groups: tuple[int]):
    first, last = record.find("#"), record.rfind("#")
    if first == -1:
        first = len(record)
    group_placements: list[list[int]] = [[] for _ in groups]
    for group_i, prev_length in enumerate(groups):
        for record_i in range(
            sum(groups[:group_i]) + group_i,
            len(record) - (sum(groups[group_i:]) + len(groups) - group_i - 1) + 1,
        ):
            end_i = record_i + prev_length
            if (
                not (group_i == 0 and first < record_i)
                and not (group_i == len(groups) - 1 and end_i <= last)
                and (record_i == 0 or record[record_i - 1] != "#")
                and not "." in record[record_i:end_i]
                and (end_i == len(record) or record[end_i] != "#")
            ):
                group_placements[group_i].append(record_i)

    combinations = [[1 for _ in group_placements[-1]]]
    for prev_placements, prev_length, next_placements in zip(
        group_placements[-2::-1],
        groups[-2::-1],
        group_placements[:0:-1],
    ):
        combinations.insert(
            0,
            [
                sum(
                    next_count
                    for next_i, next_count in zip(next_placements, combinations[0])
                    if prev_i + prev_length < next_i
                    and not "#" in record[prev_i + prev_length + 1 : next_i]
                )
                for prev_i in prev_placements
            ],
        )

    return combinations


def run(input_data: str):
    part1, part2 = 0, 0

    input_lines = input_data.splitlines()
    # output = []
    for line in input_lines:
        record, groups = tuple((line.split()))
        groups = tuple(int(g) for g in groups.split(","))
        arrangements = df_search(record, groups)
        part1 += len(arrangements)

        # combinations = find_combinations(record, groups)
        combinations = find_combinations("?".join([record] * 5), groups * 5)
        part2 += sum(combinations[0])

    #     if len(arrangements) != sum(combinations[0]):
    #         output.extend(
    #             [
    #                 "".join(str(i % 10) for i, _ in enumerate(record)),
    #                 f"{record} {groups}",
    #                 "\n".join(arrangements),
    #                 "\n".join(str(gp) for gp in group_placements),
    #                 "\n".join(str(a) for a in combinations),
    #                 f"{len(arrangements)}|{sum(combinations[0])}",
    #             ]
    #         )
    # with open("output.txt", "w") as file:
    #     [print(line, file=file) for line in output]
    return part1, part2
