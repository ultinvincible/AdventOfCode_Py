import sys
from typing import Self

from helper import dijkstra


class Burrow_Map(tuple):
    is_room = [i in (2, 4, 6, 8) for i in range(11)]
    correct_room = {amp_type: amp_type * 2 for amp_type in range(1, 5)}
    cost: dict[int, int] = {amp_type: 10 ** (amp_type - 1) for amp_type in range(1, 5)}

    def __new__(cls, input_map: list[list[tuple[int, ...] | int]]) -> Self:
        return tuple.__new__(
            cls,
            (col if not type(col) is list else tuple(col) for col in input_map),
        )

    def __init__(self, _) -> None:
        super().__init__()

    def __getitem__(self, index: int) -> int:
        column = super().__getitem__(index)
        if self.is_room[index]:
            return column[-1] if column else 0
        return column

    def room(self, col: int) -> tuple[int, ...]:
        assert self.is_room[col]
        return super().__getitem__(col)

    def __str__(self) -> str:
        return "".join(
            (
                (chr(ord("A") + column - 1) if column != 0 else ".")
                if not self.is_room[col]
                else f" <{''.join(chr(ord('A') + amp - 1) for amp in column[::-1]):>2}< "
            )
            for col, column in enumerate(self)
        )


def moves(burrow_map: Burrow_Map, room_depth=2):
    room_moves: list[tuple[int, int]] = []
    hallway_moves: list[tuple[int, int]] = []
    reachable_rooms: list[int] = []
    # reachable hallway columns:
    reachable_hwcs: list[int] = []
    # previous hallway amphipod column:
    prev_hw_amp_col = -1

    # check unblocked
    for current_col, amphipod_type in enumerate(burrow_map):
        if not Burrow_Map.is_room[current_col] and (
            amphipod_type != 0 or current_col == 10
        ):
            check_into_room = [room for room in reachable_rooms if burrow_map[room]]
            if prev_hw_amp_col != -1:
                check_into_room.append(prev_hw_amp_col)
            if amphipod_type != 0:
                check_into_room.append(current_col)
            else:
                reachable_hwcs.append(current_col)

            for source_col in check_into_room:
                source_type = burrow_map[source_col]
                correct_room = burrow_map.correct_room[source_type]
                if (
                    source_col != correct_room
                    and prev_hw_amp_col < correct_room < current_col
                    and all(
                        room_amphipod == source_type
                        for room_amphipod in burrow_map.room(correct_room)
                    )
                ):
                    room_moves.append((source_col, correct_room))

            hallway_moves.extend(
                (room_col, hallway_col)
                for room_col in reachable_rooms
                for hallway_col in reachable_hwcs
                if any(
                    amphipod != room_col // 2 for amphipod in burrow_map.room(room_col)
                )
            )

            reachable_hwcs.clear()
            reachable_rooms.clear()
            prev_hw_amp_col = current_col
        else:
            (
                reachable_rooms if burrow_map.is_room[current_col] else reachable_hwcs
            ).append(current_col)

    result: list[tuple[int, Burrow_Map]] = []
    for move_list in room_moves, hallway_moves:
        for source_col, dest_col in move_list:
            amphipod_type = burrow_map[source_col]
            if amphipod_type == 0 or (
                burrow_map[dest_col] != 0
                and len(burrow_map.room(dest_col)) == room_depth
            ):
                continue

            new_map = [
                column if not burrow_map.is_room[col] else list(column)
                for col, column in enumerate(burrow_map)
            ]
            if burrow_map.is_room[source_col]:
                new_map[source_col].pop()
            else:
                new_map[source_col] = 0
            distance = abs(source_col - dest_col)
            for col in (source_col, dest_col):
                if burrow_map.is_room[col]:
                    distance += room_depth - len(new_map[col])
            if burrow_map.is_room[dest_col]:
                new_map[dest_col].append(amphipod_type)
            else:
                new_map[dest_col] = amphipod_type

            result.append(
                (
                    distance * burrow_map.cost[burrow_map[source_col]],
                    Burrow_Map(new_map),
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
    part1, _ = dijkstra(
        StartMap(lines), moves, lambda burrow_map: burrow_map == EndMap(lines)
    )
    lines2 = lines[:3] + insert_lines + lines[3:]
    end_map = EndMap(lines2)
    part2, state_tree = dijkstra(
        StartMap(lines2),
        lambda burrow_map: moves(burrow_map, 4),
        lambda burrow_map: burrow_map == (end_map),
    )

    # with open("output", "w") as file:
    #     std = sys.stdout
    #     sys.stdout = file
    #     burrow_map = end_map
    #     while True:
    #         cost, parent_map = state_tree[burrow_map]
    #         print(f"^ {burrow_map}", cost, sep="| ")
    #         if not parent_map:
    #             break
    #         burrow_map = parent_map
    #     sys.stdout = std

    return part1, part2


def StartMap(lines):
    return Burrow_Map(
        (
            0
            if not Burrow_Map.is_room[col - 1]
            else tuple(ord(line[col]) - ord("A") + 1 for line in lines[-2:1:-1])
        )
        for col in range(1, len(lines[0]) - 1)
    )


def EndMap(lines):
    return Burrow_Map(
        (
            0
            if not Burrow_Map.is_room[col - 1]
            else tuple(col // 2 for _ in range(len(lines) - 3))
        )
        for col in range(1, len(lines[0]) - 1)
    )
