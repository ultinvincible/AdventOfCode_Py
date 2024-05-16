import math


def run(input_data: str):
    input_lines = input_data.splitlines()
    module_by_name: dict[str, bool | dict] = {}
    receiver_names: dict[str, list[str]] = {}
    for line in input_lines:
        current_module, receiver_list = tuple(line.split(" -> "))
        module_type, module_name = (
            (current_module[0], current_module[1:])
            if current_module[0] in "%&"
            else (None, current_module)
        )
        if module_type:
            module_by_name[module_name] = False if module_type == "%" else {}
        receiver_names[module_name] = receiver_list.split(", ")

    for module_name, new_receivers in receiver_names.items():
        for receiver_name in new_receivers:
            try:
                module_by_name[receiver_name][module_name] = False
            except (KeyError, TypeError):
                pass

    def df_search(name: str, path: list[str] = None):
        if not path:
            path = []
        path.append(name)

        result = []
        for sender, receiver_list in receiver_names.items():
            if name in receiver_list and not sender in path:
                result.extend(df_search(sender, path.copy()))
        return result or [path]

    paths = df_search("rx")
    paths.sort(key=lambda path: (path[:4], len(path)))

    count = {False: 0, True: 0}
    cycle = {}
    cycle_checks = list(set(path[2] for path in paths))
    output = []
    for press in range(1, 2**63):
        count[False] += 1
        to_receive = [("broadcaster", False)]
        while to_receive:
            new_pulses = []
            for module_name, is_high_pulse in to_receive:
                new_receivers = receiver_names[module_name]
                count[is_high_pulse] += len(new_receivers)
                for receiver_name in new_receivers:
                    if (module := module_by_name.get(receiver_name, None)) is None:
                        continue
                    if type(module) is bool:
                        if not is_high_pulse:
                            module_by_name[receiver_name] = not module
                            new_pulses.append((receiver_name, not module))
                    else:
                        module[module_name] = is_high_pulse
                        new_pulses.append((receiver_name, not all(module.values())))
            for name in cycle_checks:
                if (name, True) in new_pulses and not name in cycle:
                    cycle[name] = press
            to_receive = new_pulses
        if press == 1000:
            part1 = count[False] * count[True]
        if press >= 1000 and len(cycle) == 4:
            break

        output.append(press)
        output.append(
            "".join(str(int(module_by_name[name])) for name in paths[6][4:-1])
        )

    with open("output2.txt", "w") as file:
        [print(line, file=file) for line in output]

    with open("output.txt", "w") as file:
        for path in paths:
            path = [
                (
                    ""
                    if (module_type := module_by_name.get(name, None)) is None
                    else "%" if type(module_type) is bool else "&"
                )
                + name
                for name in path
            ]
            print(
                "|".join(path[:2]),
                "|".join(path[2:4]),
                "|".join(path[4:]).rjust(59),
                sep=" | ",
                file=file,
            )
        print(cycle, file=file)

    return part1, math.lcm(*cycle.values())
