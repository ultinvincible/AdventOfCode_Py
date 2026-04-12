def run(input_data: str):
    part1, part2 = 0, 0

    input_grid = input_data.splitlines()
    beam_cols_timelines = {input_grid[0].index("S"): 1}
    for line in input_grid[1:]:
        new_timelines = dict(beam_cols_timelines)
        for beam_col, timelines in beam_cols_timelines.items():
            if line[beam_col] != "^":
                continue
            new_timelines.pop(beam_col)
            for new_col in (beam_col - 1, beam_col + 1):
                new_timelines[new_col] = new_timelines.get(new_col, 0) + timelines
            part1 += 1
        beam_cols_timelines = new_timelines
    part2 = sum(beam_cols_timelines.values())

    return part1, part2
