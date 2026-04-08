import math


def run(input_data: str):
    part1, part2 = 0, 0

    range_list = input_data.split(",")
    for id_range in range_list:
        id1, id2 = tuple(map(int, id_range.split("-")))
        for id in range(id1, id2 + 1):
            digits = math.floor(math.log10(id)) + 1
            if digits % 2 == 0 and id // 10 ** (digits / 2) == id % 10 ** (digits / 2):
                part1 += id
                part2 += id
                continue

            for num_repetition in range(3, digits + 1):
                if digits % num_repetition != 0:
                    continue
                block_num_digits = digits // num_repetition

                current_block = id % 10**block_num_digits
                do_repeat = True
                for i in range(num_repetition - 1):
                    next_block = (
                        id // 10 ** (block_num_digits * (i + 1)) % 10**block_num_digits
                    )
                    if current_block != next_block:
                        do_repeat = False
                        break
                    current_block = next_block

                if do_repeat:
                    part2 += id
                    break

    return part1, part2
