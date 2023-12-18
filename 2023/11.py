def run(input_data: str):
    part1 = 0
    part2 = 0
    star_map = [list(s) for s in input_data.splitlines()]
    galaxies = []
    empty_rows = [True for _ in range(len(star_map))]
    empty_cols = [True for _ in range(len(star_map[0]))]

    for row, line in enumerate(star_map):
        for col, point in enumerate(line):
            if point == "#":
                galaxies.append((row, col))
                empty_rows[row] = False
                empty_cols[col] = False
    empty_rows = [r for r in range(len(empty_rows)) if empty_rows[r]]
    empty_cols = [c for c in range(len(empty_cols)) if empty_cols[c]]

    for g, (row1, col1) in enumerate(galaxies):
        # print(f"{row1,col1}: ")
        for row2, col2 in galaxies[g + 1 :]:
            (row_min, row_max) = (min((row1, row2)), max((row1, row2)))
            (col_min, col_max) = (min((col1, col2)), max((col1, col2)))
            distance = row_max - row_min + col_max - col_min
            empty = 0
            for r in empty_rows:
                if row_min < r < row_max:
                    empty += 1
            for c in empty_cols:
                if col_min < c < col_max:
                    empty += 1
            part1 += distance + empty
            part2 += distance + empty * 999999
            # print(f"  {row2,col2}:{distance}")

    return part1, part2
