def run(input_data: str):
    part1 = 0
    part2 = 0
    cubes = ['red', 'green', 'blue']
    number = [12, 13, 14]
    for i, line in enumerate(input_data.splitlines()):
        possible = True
        minimum = [0, 0, 0]
        for grab in line[line.index(':') + 2:].split('; '):
            for s in grab.split(', '):
                color = s.split(' ')
                count = int(color[0])
                index = cubes.index(color[1])
                if count > number[index]:
                    possible = False

                if count > minimum[index]:
                    minimum[index] = count
        if possible:
            part1 += i + 1
        part2 += minimum[0] * minimum[1] * minimum[2]
    return part1, part2
