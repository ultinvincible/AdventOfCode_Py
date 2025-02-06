def run(input_data: str):
    part1, part2 = 0, 0

    input_lines = input_data.splitlines()
    list1, list2 = [], []
    for line in input_lines:
        num1, num2 = map(int, tuple(line.split()))
        list1.append(num1)
        list2.append(num2)
    list1.sort()
    list2.sort()
    for num1, num2 in zip(list1, list2):
        part1 += abs(num1 - num2)

    count = {}
    for num2 in list2:
        count[num2] = count.get(num2, 0) + 1
    for num1 in list1:
        part2 += num1 * count.get(num1, 0)

    return part1, part2
