def run(input_data: str):
    fish_count = [input_data.count(str(i)) for i in range(9)]
    for day in range(256):
        if day == 80:
            part1 = sum(fish_count)
        create = fish_count.pop(0)
        fish_count[6] += create
        fish_count.append(create)
    part2 = sum(fish_count)

    # fish_list = [int(fish) for fish in input_data.split(",")]
    # for day in range(256):
    #     if day == 80:
    #         part1 = len(fish_list)
    #         print(part1)
    #     new_fish_list = []
    #     for fish in fish_list:
    #         if fish == 0:
    #             new_fish_list.extend([6, 8])
    #         else:
    #             new_fish_list.append(fish - 1)
    #     fish_list = new_fish_list
    #     with open("output.txt", "w") as file:
    #         print(day, len(fish_list), file=file)
    # part2 = len(fish_list)

    return part1, part2
