symbols = "#.?"


def run(input_data: str):
    part1 = 0
    part2 = 0
    for i, line in enumerate(input_data.splitlines()):
        split = line.split()
        records = list(split[0])
        groups = [int(i) for i in split[1].split(",")]
        arrangements = find_arrangements(records, groups)
        part1 += len(arrangements)

        # new_records = [list(records) for _ in (0, 1)]
        # new_records[0].append("?")
        # new_records[1].insert(0, "?")
        # new_arrangements_list = [
        #     find_arrangements(record, groups) for record in new_records
        # ]
        # a = 0 if len(new_arrangements_list[0]) >= len(new_arrangements_list[1]) else 1
        # new_arrangements = new_arrangements_list[a]
        # mismatch = len([arr for arr in arrangements if arr[-a] == "#"]) * len(
        #     [arr for arr in new_arrangements if arr[a - 1] == "#"]
        # )
        # total_arr = len(arrangements) * int(
        #     math.pow(len(new_arrangements) - mismatch, 4)
        # )
        # part2 += total_arr

        records.append("?")
        records2 = (records * 5)[:-1]
        groups2 = groups * 5

        placable_list = []
        i = 0
        while i < len(records2):
            if records2[i] != ".":
                for ii in range(i, len(records2)):
                    if ii == len(records2) - 1 or records2[ii + 1] == ".":
                        placable_list.append((i, ii))
                        i = ii
                        break
            i += 1
        groups_ranges = [[0]]
        for group in groups2[:-1]:
            groups_ranges.append([groups_ranges[-1][0] + group + 1])
        groups_ranges[-1].append(len(records2) - groups2[-1])
        for g, group in enumerate(groups2[-2::-1]):
            groups_ranges[-2 - g].append(groups_ranges[-1 - g][1] - group - 1)

        group_placables = []
        for group, group_range in zip(groups2, groups_ranges):
            group_placables.append([])
            for placable in placable_list:
                if group_range[1] < placable[0]:
                    break
                min_start = max(group_range[0], placable[0])
                max_start = min(group_range[1], placable[1])
                if min_start <= max_start:
                    group_placables[-1].extend(range(min_start, max_start + 1))
        arrangements2 = []
        for group, gp1, gp2 in zip(
            groups2[:-1], group_placables[:-1], group_placables[1:]
        ):
            arrangements2.append([])
            # cache = {}
            for g1 in gp1:
                index_valid = len(gp2)
                for i2, g2 in enumerate(gp2):
                    if g1 + group < g2:
                        index_valid = i2
                        break
                # if index_valid in cache:
                #     arr_count = cache[index_valid]
                # else:
                #     arr_count = sum(arrangements2[-2][:index_valid])
                #     cache[index_valid] = arr_count
                if index_valid != len(gp2):
                    arrangements2[-1].append(index_valid)
        # for g in range(len(arrangements2) - 2, -1, -1):
        #     delete = len(arrangements2[g])
        #     for a, arr in enumerate(arrangements2[g]):
        #         if arr >= len(arrangements2[g + 1]):
        #             delete = a
        #             break
        #     arrangements2[g] = arrangements2[g][:delete]

        arrangements2_count = sum(arrangements2[-1])

        arrangements_test = find_arrangements(records2, groups2)
        test = [{} for g in groups2]
        for arr in arrangements_test:
            for i, index in enumerate(arr):
                if index in test[i]:
                    test[i][index] += 1
                else:
                    test[i][index] = 1

        part2 += len(arrangements_test)

        # for i in range(len(records2)):
        #     print((i + 1) % 10, end="")
        # print()
        # print("".join(records2) + "  " + ",".join([str(g) for g in groups2]))
        # # for arr in arrangements_test[:100]:
        # #     print(arr)
        # print()
    return part1, part2


def find_arrangements(arrangement, groups, index=0, starts=[]):
    if len(groups) == 0:
        for c, s in enumerate(arrangement[index + 1 :]):
            if s == "?":
                arrangement[index + 1 + c] = "."
            elif s == "#":
                return []
        return [starts]
    if index == len(arrangement):
        return []

    if arrangement[index] == ".":
        for i, s in enumerate(arrangement[index + 1 :]):
            if s != ".":
                index += i + 1
                break
        if index == len(arrangement) - 1 and arrangement[index] == ".":
            index += 1
        new_arrangements_list = [[arrangement, groups, index, starts]]
    elif arrangement[index] == "#":
        end = index + groups[0]
        if end > len(arrangement) or (
            end < len(arrangement) and arrangement[end] == "#"
        ):
            return []
        for s in range(index + 1, index + groups[0]):
            if arrangement[s] == ".":
                return []
            if arrangement[s] == "?":
                arrangement[s] = "#"
        if end < len(arrangement):
            arrangement[end] = "."
        starts.append(index)
        new_arrangements_list = [[arrangement, groups[1:], end + 1, starts]]
    else:
        new_arrangements_list = [
            [list(arrangement), groups, index, list(starts)] for a in range(2)
        ]
        for a in (0, 1):
            new_arrangements_list[a][0][index] = symbols[a]

    result = []
    for arr in new_arrangements_list:
        # print(("".join(arr[0]), arr[1], arr[2], arr[3]))
        result.extend(find_arrangements(arr[0], arr[1], arr[2], arr[3]))
    return result
