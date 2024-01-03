import re
import operator

ops = {">": operator.gt, "<": operator.lt}
opposite = {">": ("<", 1), "<": (">", -1)}


def run(input_data: str):
    part1 = 0
    part2 = 0
    workflows = {}
    sections = input_data.split("\n\n")
    for i, line in enumerate(sections[0].splitlines()):
        split = re.split(r"[{},]", line)
        name = split.pop(0)
        split = [re.split(r"([<>:])", s) for s in split[:-1]]
        workflows[name] = split
    for part in sections[1].splitlines():
        split = [s for s in re.split(r"[{}=,]", part) if s != ""]
        ratings = {}
        for categ, score in zip(split[0:-1:2], split[1::2]):
            ratings[categ] = int(score)

        current = workflows["in"]
        while True:
            for condition in current:
                if len(condition) == 1:
                    current = condition[0]
                elif ops[condition[1]](ratings[condition[0]], int(condition[2])):
                    current = condition[-1]
                    break
            if current == "R":
                break
            if current == "A":
                for score in ratings.values():
                    part1 += score
                break
            current = workflows[current]

    # def print_tree(name="in", level=0):
    #     if name in "AR":
    #         print("| " * level + name)
    #         return
    #     workflow = workflows[name]
    #     for i, flow in enumerate(workflow):
    #         if len(flow) != 1:
    #             print("| " * (level + i) + " ".join(flow[:3]))
    #         else:
    #             i -= 1
    #         print_tree(flow[-1], level + i + 1)

    # print_tree()

    accepted_paths = []

    def df_search(path=[], name="in", index=0):
        if name == "R":
            return None
        if name == "A":
            return []
        flow = workflows[name][index]
        if len(flow) == 1:
            return df_search(path, flow[0])
        flow[2] = int(flow[2])

        path_true = list(path)
        path_true.append(flow[:3])
        if_true = df_search(path_true, flow[-1])

        path_false = list(path)
        new_flow = list(flow)
        new_flow[1], i = opposite[flow[1]]
        new_flow[2] += i
        path_false.append(new_flow[:3])
        if_false = df_search(path_false, name, index + 1)

        if if_true == if_false == []:
            return []
        if if_true == []:
            accepted_paths.append(path_true)
        if if_false == []:
            accepted_paths.append(path_false)

    df_search()
    # for path in accepted_paths:
    #     print(path)
    accepted_combinations = []
    for path in accepted_paths:
        accepted = {}
        for rating in "xmas":
            accepted[rating] = [0, 4001]
        for step in path:
            rating, sign, value = tuple(step)
            if sign == ">":
                accepted[rating][0] = max(accepted[rating][0], value)
            else:
                accepted[rating][1] = min(accepted[rating][1], value)
        accepted_combinations.append(accepted)
    # for cbnt in accepted_combinations:
    #     print("".join(f"{str(item): <20}" for item in cbnt.items()))
    for cbnt in accepted_combinations:
        no_cbnts = 1
        for acc_range in cbnt.values():
            no_cbnts *= acc_range[1] - acc_range[0] - 1
        part2 += no_cbnts

    return part1, part2
