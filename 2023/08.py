import math
import re


def run(input_data: str):
    part2 = 0
    split = input_data.split('\n\n')
    instructions = [0 if i == 'L' else 1 for i in split[0]]
    nodes = {}
    for i, line in enumerate(split[1].splitlines()):
        split = [s for s in re.split('[ =(,)]', line) if s != '']
        nodes[split[0]] = (split[1], split[2])
    current = 'AAA'
    instr_i = 0
    step = 0
    while current != 'ZZZ':
        current = nodes[current][instructions[instr_i]]
        instr_i = instr_i + 1 if instr_i != len(instructions) - 1 else 0
        step += 1
    part1 = step

    loops = []
    for current in [n for n in nodes.keys() if n[2] == 'A']:
        instr_i = 0
        step = 0
        loop_start = -1
        while True:
            if current[2] == 'Z':
                if loop_start == -1:
                    loop_start = step
                else:
                    break
            current = nodes[current][instructions[instr_i]]
            instr_i = instr_i + 1 if instr_i != len(instructions) - 1 else 0
            step += 1
        loops.append((loop_start, step - loop_start))
    part2 = math.lcm(*tuple([loop[0] for loop in loops]))

    return part1, part2
