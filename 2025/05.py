from helper import ranges_merge


def run(input_data: str):
    part1, part2 = 0, 0

    fresh_input, available_input = map(str.splitlines, tuple(input_data.split("\n\n")))
    fresh_db = []
    for line in fresh_input:
        fresh_db.append(tuple(map(int, line.split("-"))))

    for line in available_input:
        ingredient = int(line)
        is_fresh = False
        for fresh_min, fresh_max in fresh_db:
            if fresh_min <= ingredient <= fresh_max:
                is_fresh = True
                break
        if is_fresh:
            part1 += 1

    fresh_merged_db = []
    for fresh_range in fresh_db:
        merge_index = -1
        for i, fresh_merged_range in enumerate(fresh_merged_db):
            merge = ranges_merge(
                fresh_merged_range,
                fresh_range if merge_index == -1 else fresh_merged_db[merge_index],
            )
            if merge:
                fresh_merged_db[i] = merge
                merge_index = i
                break
        if merge_index == -1:
            fresh_merged_db.append(fresh_range)
            continue

        new_merged_db = [fresh_merged_db[merge_index]]
        for fresh_merged_range in fresh_merged_db[merge_index + 1 :]:
            merge = ranges_merge(fresh_merged_db[merge_index], fresh_merged_range)
            if merge:
                new_merged_db[0] = merge
            else:
                new_merged_db.append(fresh_merged_range)
        fresh_merged_db = fresh_merged_db[:merge_index] + new_merged_db

    part2 = sum(range_max - range_min + 1 for (range_min, range_max) in fresh_merged_db)
    return part1, part2
