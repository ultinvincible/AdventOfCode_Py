def run(input_data: str):
    part1, part2 = 0, 0

    input_lines = input_data.splitlines()
    enable = True
    for line in input_lines:
        prev_i = -1
        prev_mul = None
        for i, char in enumerate(line):
            if line[i : i + 4] == "do()":
                enable = True
            elif line[i : i + 7] == "don't()":
                enable = False

            if line[i : i + 4] == "mul(":
                prev_i = i + 4
            elif char in [",", ")"]:
                if prev_i != -1:
                    if line[prev_i:i].isdigit():
                        num = int(line[prev_i:i])
                        if prev_mul is None:
                            prev_mul = num
                        else:
                            mul = prev_mul * num
                            part1 += mul
                            if enable:
                                part2 += mul
                            prev_mul = None
                        prev_i = i + 1 if char == "," else -1
                    else:
                        if char == ")":
                            prev_mul = None
                        prev_i = -1
            elif not char.isdigit():
                if prev_i != -1:
                    prev_mul = None

    return part1, part2
