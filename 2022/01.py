def run(input_data: str):
    sections = input_data.split("\n\n")
    elves = [
        sum(int(calories) for calories in sect.split("\n") if calories)
        for sect in sections
    ]
    elves.sort()
    return elves[-1], elves[-1] + elves[-2] + elves[-3]
