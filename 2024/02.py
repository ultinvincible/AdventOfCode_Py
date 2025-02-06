def find_bad_diff(nums: list[int]):
    prev = None
    for i, (num1, num2) in enumerate(zip(nums[:-1], nums[1:])):
        diff = num1 - num2
        if not (1 <= abs(diff) <= 3 and (prev is None or prev * diff > 0)):
            return i
        prev = diff
    return None


def remove_unsafe(nums: list[int], unsafe=False):
    i = find_bad_diff(nums)
    if i is not None:
        if unsafe:
            return None
        check_remove = [i, i + 1]
        if i == 1:
            check_remove.insert(0, 0)
        for rm_i in check_remove:
            new_nums = list(nums)
            new_nums.pop(rm_i)
            if remove_unsafe(new_nums, True) is not None:
                return new_nums
        return None
    return nums


def run(input_data: str):
    part1, part2 = 0, 0

    input_lines = input_data.splitlines()
    for line in input_lines:
        if not line:
            continue
        nums = [int(s) for s in line.split()]
        removed = remove_unsafe(nums)

        if removed == nums:
            part1 += 1
        if removed is not None:
            part2 += 1

    return part1, part2
