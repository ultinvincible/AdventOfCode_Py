from helper import directions_2d

symbols = "RULD"


def run(input_data: str):
    part1 = 0
    part2 = 0
    dig_plan, dig_plan2 = [], []
    drts_2d = directions_2d()
    for line in input_data.splitlines():
        drt, dist, color = tuple(line.split())
        dig_plan.append((drts_2d[symbols.index(drt)], int(dist)))
        dig_plan2.append((drts_2d[(4 - int(color[7])) % 4], int(color[2:7], 16)))

    rows = {0: []}
    current = [0, 0]
    for i, (drt, dist) in enumerate(dig_plan):
        move = 0 if drt[0] != 0 else 1
        new_coord = current[move] + drt[move] * dist
        if move == 0:
            for row in range(
                current[move] + drt[move], new_coord + drt[move], drt[move]
            ):
                if row not in rows:
                    rows[row] = []
                if row != new_coord:
                    rows[row].append((current[1], current[1]))
        else:
            col_range = sorted((current[move], new_coord))
            col_range.append(
                dig_plan[i - 1][0]
                == dig_plan[(i + 1) if i != len(dig_plan) - 1 else 0][0]
            )
            rows[current[0]].append(tuple(col_range))
        current[move] = new_coord

    area = 0
    for cols in rows.values():
        cols.sort()
        prev = None
        row_area = 0
        # test = ""
        # i = cols[0][0]
        # outside = True
        for col_range in cols:
            # test += ("." if outside else "_") * (col_range[0] - i) + "#" * (
            #     col_range[1] - col_range[0] + 1
            # )
            # i = col_range[1] + 1

            if len(col_range) != 2 and not col_range[2]:
                if prev is None:
                    row_area += col_range[1] - col_range[0] + 1
            else:
                if prev is None:
                    prev = col_range[0]
                else:
                    row_area += col_range[1] - prev + 1
                    prev = None
                # outside = not outside
        area += row_area
        # if test.count("#") + test.count("_") != lava:
        #     pass

    part1 = area

    # file = open("output.py", "w")
    # row = min(rows.keys())
    # min_col = min(row[0][0] for row in rows.values())
    # while row in rows:
    #     i = min_col
    #     outside = True
    #     for col_range in rows[row]:
    #         file.write(
    #             ("." if outside else "_") * (col_range[0] - i)
    #             + "#" * (col_range[1] - col_range[0] + 1)
    #         )
    #         if len(col_range) == 2 or col_range[2]:
    #             outside = not outside
    #         i = col_range[1] + 1
    #     file.write("\n")
    #     row += 1
    # # file = open("output.py", "r")
    # # read: str = file.read()
    # # print(read.count("#") + read.count("_"))
    # file.close()

    rows, cols = {}, {}
    current = [0, 0]
    for i, (drt, dist) in enumerate(dig_plan2):
        move = 0 if drt[0] != 0 else 1
        line = [current[move]] * 2
        line.append(
            dig_plan2[i - 1][0]
            == dig_plan2[(i + 1) if i != len(dig_plan2) - 1 else 0][0]
        )
        new_i = (drt[move] + 1) // 2
        line[new_i] += drt[move] * dist
        to_append = rows if move == 1 else cols
        if current[1 - move] not in to_append:
            to_append[current[1 - move]] = []
        to_append[current[1 - move]].append(tuple(line))
        current[move] = line[new_i]
    for row, row_edges in rows.items():
        for col, col_lines in cols.items():
            for start, end, _ in col_lines:
                if start < row < end:
                    row_edges.append((col, col, True))
        row_edges.sort()
    rows = sorted(rows.items())

    area = []
    lines = []
    for row, row_edges in rows:
        new_lines = []
        outside = True
        for start, end, switch in row_edges:
            if not switch and outside:
                line_is_end = False
                for line_row, line_start, line_end in lines:
                    if (line_start, line_end) == (start, end):
                        area.append((line_end, line_start, row, line_row))
                        line_is_end = True
                        break
                if not line_is_end:
                    new_lines.extend([start, end])
                continue
            for line_row, line_start, line_end in lines:
                if end < line_start:
                    break
                if not switch and not outside:
                    if line_end == start:
                        area.append((line_end, line_start, row - 1, line_row))
                        break
                    if line_start < start and end < line_end:
                        new_lines.extend([start, end])
                        area.append((end - 1, start + 1, row, row))
                        break
                if line_start in (start, end):
                    new_lines.append(start if line_start == end else end)
                if line_end in (start, end):
                    new_lines.append(start if line_end == end else end)
                    area.append((line_end, line_start, row - 1, line_row))
                if start != end and (line_start == start or line_end == end):
                    area.append((end, start + 1, row, row))
            outside = not outside if switch else outside
        lines = []
        for start, end in zip(new_lines[::2], new_lines[1::2]):
            lines.append((row, start, end))
        pass
    for c2, c1, r2, r1 in area:
        part2 += (c2 - c1 + 1) * (r2 - r1 + 1)

    # with open("output.py", "r") as file:
    #     dig_map = [list(s) for s in file.readlines()]
    # for c2, c1, r2, r1 in area:
    #     for r in range(r1, r2 + 1):
    #         for c in range(c1, c2 + 1):
    #             dig_map[r - rows[0][0]][c - min_col] = "X"
    # with open("output.py", "w") as file:
    #     for row in dig_map:
    #         file.write(''.join(row))

    return part1, part2
