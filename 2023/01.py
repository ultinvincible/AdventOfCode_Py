def run(input_data: str):
    part1 = 0
    part2 = 0
    for line in input_data.splitlines():
        value = ""
        for char in line:
            if char.isdecimal():
                value += char
                break
        for char in reversed(line):
            if char.isdecimal():
                value += char
                break
        part1 += int(value)

    digits = [str(i) for i in range(10)]
    digits.extend(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    )
    for line in input_data.splitlines():
        left = "", len(line)
        right = "", -1
        for d in digits:
            index = line.find(d)
            if index != -1 and index < left[1]:
                left = d, index
            index = line.rfind(d)
            if index != -1 and index > right[1]:
                right = d, index
        value1 = left[0] if left[0].isdecimal() else str(digits.index(left[0]) - 9)
        value2 = right[0] if right[0].isdecimal() else str(digits.index(right[0]) - 9)
        part2 += int(value1 + value2)
    return part1, part2
