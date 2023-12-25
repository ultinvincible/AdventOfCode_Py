import re


def run(input_data: str):
    part1 = 0
    part2 = 0
    split = input_data[:-1].split(",")
    boxes: dict[int, (list, list)] = {}
    for _, string in enumerate(split):
        part1 += hash_alg(string)

        split = tuple(re.split("[-=]", string))
        (label, focal) = split
        box_number = hash_alg(label)
        if focal == "":
            if box_number in boxes:
                try:
                    l = boxes[box_number][0].index(label)
                except ValueError:
                    continue
                boxes[box_number][0].pop(l)
                boxes[box_number][1].pop(l)
        else:
            if box_number not in boxes:
                boxes[box_number] = ([], [])
            try:
                l = boxes[box_number][0].index(label)
            except ValueError:
                boxes[box_number][0].append(label)
                boxes[box_number][1].append(int(focal))
                continue
            boxes[box_number][1][l] = int(focal)
    for box_number, (_, focals) in boxes.items():
        for i, f in enumerate(focals):
            part2 += (1 + box_number) * (i + 1) * f

    return part1, part2


def hash_alg(string):
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256
    return value
