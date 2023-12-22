import math


def run(input_data: str):
    part1 = 1
    lines = input_data.splitlines()
    time = [int(value) for value in lines[0].split()[1:]]
    distance = [int(value) for value in lines[1].split()[1:]]
    for s, t in zip(distance, time):
        ways = calc_ways(s, t)
        part1 *= ways

    time = int("".join([str(t) for t in time]))
    distance = int("".join([str(s) for s in distance]))
    part2 = calc_ways(distance, time)

    return part1, part2


# t(T-t)=S => t^2 -Tt + S = 0 => t = (T +- sqrt(T^2 - 4S))/2
def calc_ways(distance, time):
    time_record = (time - math.sqrt(math.pow(time, 2) - 4 * distance)) / 2
    ways = (math.ceil(time / 2) - math.ceil(time_record)) * 2
    if time % 2 == 0:
        ways += 1
    if float.is_integer(time_record):
        ways -= 2
    return ways
