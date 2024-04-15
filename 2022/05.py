import copy


def run(input_data: str):
    sections = input_data.split("\n\n")
    stacks: list[list[str]] = []
    for line in sections[0].splitlines()[-2::-1]:
        for col, char in enumerate(line[1::4]):
            if char == " ":
                continue
            try:
                stacks[col].append(char)
            except IndexError:
                stacks.append([char])

    stacks1 = copy.deepcopy(stacks)
    stacks2 = copy.deepcopy(stacks)
    for line in sections[1].splitlines():
        move, from_, to = tuple(int(s) for s in line.split() if s.isdecimal())
        from_ -= 1
        to -= 1

        stacks1[to] += stacks1[from_][-1 : -move - 1 : -1]
        stacks1[from_] = stacks1[from_][:-move]

        stacks2[to] += stacks2[from_][-move:]
        stacks2[from_] = stacks2[from_][:-move]

    return "".join(stk[-1] for stk in stacks1), "".join(stk[-1] for stk in stacks2)
