from helper import dijkstra

IsRoom = [i in (2, 4, 6, 8) for i in range(11)]
CorrectRoom = {amp_type: amp_type * 2 for amp_type in range(1, 5)}
Cost = {amp_type: 10 ** (amp_type - 1) for amp_type in range(1, 5)}


def moves(burrow_map: tuple[int, tuple[int, ...]], room_depth=2):
    room_moves: list[tuple[int, int]] = []
    hallway_moves: list[tuple[int, int]] = []
    reachable_rooms: list[int] = []
    # reachable hallway columns:
    reachable_hwcs: list[int] = []
    # previous hallway amphipod index:
    prev_hw_amp_i = -1

    # check unblocked
    for col_i, source_col in enumerate(burrow_map):
        if not IsRoom[col_i] and (source_col != 0 or col_i == 10):
            check_into_room = [room for room in reachable_rooms if burrow_map[room]]
            if prev_hw_amp_i != -1:
                check_into_room.append(prev_hw_amp_i)
            if source_col != 0:
                check_into_room.append(col_i)
            else:
                reachable_hwcs.append(col_i)

            for source_i in check_into_room:
                source_type = burrow_map[source_i]
                if not type(source_type) is int:
                    source_type = source_type[-1]
                dest_room = CorrectRoom[source_type]
                if (
                    source_i != dest_room
                    and prev_hw_amp_i < dest_room < col_i
                    and all(
                        room_amphipod == source_type
                        for room_amphipod in burrow_map[dest_room]
                    )
                ):
                    room_moves.append((source_i, dest_room))

            hallway_moves.extend(
                (room_i, hallway_i)
                for room_i in reachable_rooms
                for hallway_i in reachable_hwcs
                if any(amphipod != room_i // 2 for amphipod in burrow_map[room_i])
            )

            reachable_hwcs.clear()
            reachable_rooms.clear()
            prev_hw_amp_i = col_i
        else:
            (reachable_rooms if IsRoom[col_i] else reachable_hwcs).append(col_i)

    result: list[tuple[int, tuple[int, tuple[int, ...]]]] = []
    for move_list in room_moves, hallway_moves:
        for source_i, dest_i in move_list:
            if not burrow_map[source_i] or (
                burrow_map[dest_i] != 0 and len(burrow_map[dest_i]) == room_depth
            ):
                continue

            new_map = [
                column if not IsRoom[col_i] else list(column)
                for col_i, column in enumerate(burrow_map)
            ]
            if IsRoom[source_i]:
                amphipod_type = new_map[source_i].pop()
            else:
                amphipod_type = new_map[source_i]
                new_map[source_i] = 0
            distance = abs(source_i - dest_i)
            for col_i in (source_i, dest_i):
                if IsRoom[col_i]:
                    distance += room_depth - len(new_map[col_i])
            if IsRoom[dest_i]:
                new_map[dest_i].append(amphipod_type)
            else:
                new_map[dest_i] = amphipod_type

            result.append(
                (
                    distance * Cost[amphipod_type],
                    tuple(
                        column if not IsRoom[col] else tuple(column)
                        for col, column in enumerate(new_map)
                    ),
                )
            )
        if result:
            break
    return result


insert_lines = [
    "  #D#C#B#A#",
    "  #D#B#A#C#",
]


def run(input_data: str):
    lines = input_data.splitlines()
    result = []
    # output = []
    for input_lines in (lines, lines[:3] + insert_lines + lines[3:]):
        room_depth = len(input_lines) - 3
        start_map = tuple(
            (
                0
                if not IsRoom[col - 1]
                else tuple(
                    ord(line[col]) - ord("A") + 1 for line in input_lines[-2:1:-1]
                )
            )
            for col in range(1, len(input_lines[0]) - 1)
        )
        end_map = tuple(
            (0 if not IsRoom[col - 1] else tuple(col // 2 for _ in range(room_depth)))
            for col in range(1, len(input_lines[0]) - 1)
        )
        part, map_tree = dijkstra(
            start_map,
            lambda burrow_map: moves(burrow_map, room_depth),
            lambda burrow_map: burrow_map == end_map,
        )
        result.append(part)

    #     if part:
    #         burrow_map = end_map
    #         while True:
    #             cost, parent_map = map_tree[burrow_map]
    #             output.append(f"{Draw(burrow_map, room_depth, parent_map)}| {cost}")
    #             if not (burrow_map := parent_map):
    #                 output.append("")
    #                 break
    #     else:
    #         for burrow_map, (cost, parent_map) in map_tree.items():
    #             output.append(Draw(burrow_map, room_depth) + " " + "<" * 7)
    #             output.append(Draw(parent_map, room_depth) + " " + f"{cost:>5} ^")
    # with open("output", "w") as file:
    #     [print(line, file=file) for line in output]

    return tuple(result)


def Amp(amphipod: int):
    return chr(ord("A") + amphipod - 1) if amphipod != 0 else "."


def Draw(
    burrow_map: tuple[int, tuple[int, ...]],
    room_depth: int,
    parent_map: tuple[int, tuple[int, ...]] | None = None,
) -> str:
    if not burrow_map:
        return str(burrow_map)
    result = [[""] for _ in range(room_depth + 1)]
    for col_i, column in enumerate(burrow_map):
        source = (
            parent_map
            and column != parent_map[col_i]
            and (IsRoom[col_i] and len(column) < len(parent_map[col_i]) or column == 0)
        )

        result[0].append("-" if IsRoom[col_i] else "*" if source else Amp(column))
        for row in range(1, room_depth + 1):
            try:
                amp = column[room_depth - row]
            except IndexError:
                amp = 0
            except TypeError:
                amp = column
            result[row].append(
                " "
                if not IsRoom[col_i]
                else "*" if source and row == room_depth - len(column) else Amp(amp)
            )
    return "\n".join("".join(line) for line in result)
