import datetime
import importlib.util
import os
import re
import sys
import time
import requests

base_url = "https://adventofcode.com/"


def run_day(year, day, measure_time=False):
    path = "Inputs"
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, f"{year}{str(day).zfill(2)}.txt")
    if not os.path.isfile(path) or os.stat(path).st_size == 0:
        with open(path, "a") as file:
            response = requests.get(
                f"{base_url}20{year}/day/{day}/input", cookies={"session": sessionToken}
            )
            file.write(response.content.decode("utf-8"))
    input_data = open(path, "r").read()

    module = sys.modules[f"20{year}.{day:02}"]
    importlib.reload(module)
    run = getattr(module, "run")
    if measure_time:
        start = time.time()
        results = run(input_data)
        end = time.time()
        return results, end - start
    return run(input_data)


if __name__ == "__main__":
    now = datetime.datetime.now()
    year = now.year - 2001
    if now.month == 12:
        year += 1
    day = 1
    with open("sessionToken") as file:
        sessionToken = file.read()

    for y in range(15, now.year - 1999):
        try:
            listdir = os.listdir(f"20{y}")
        except FileNotFoundError:
            continue
        for filename in listdir:
            if filename[:2].isdecimal():
                d = int(filename[:2])
                if not 1 <= d <= 25:
                    continue
                importlib.import_module(f"20{y}.{d:02}")

    while True:
        options = input(f"Run [year] day ({year} {day:02} or {day}): ").split()
        try:
            day = int(options[-1])
            assert 1 <= day <= 25
        except (IndexError, AssertionError):
            print("Invalid options provided. Exiting.")
            break

        if len(options) > 1:
            option_year = int(options[0])
            if 15 <= option_year <= now.year - 2000:
                year = option_year

        year_path = f"20{year}"
        path = os.path.join(year_path, f"{day:02}.py")
        if not os.path.isfile(path) or os.stat(path).st_size == 0:
            template = open("template.py", "r").read()
            if not os.path.exists(year_path):
                os.mkdir(year_path)
            open(path, "a").write(template)
            print("File created.")
            break

        result, runtime = run_day(year, day, True)
        print(f"{result[0] or 'Not implemented.'}\n{result[1] or 'Not implemented.'}")

        if not any(result):
            continue
        print(f"Runtime: {round(runtime, 2)} s. ", end="")
        if input("Input 'y' to submit: ") == "y":
            part = 2 if result[1] else 1
            data = {"level": part, "answer": result[part - 1]}
            headers = {
                "User-Agent": "Python 3.12",
                "From": "trinhminhkhanh278@gmail.com",
            }
            response = requests.post(
                f"{base_url}20{year}/day/{day}/answer",
                data=data,
                cookies={"session": sessionToken},
                headers=headers,
            )
            html = re.split(
                "<main>\n<article><p>|</p></article>\n</main>",
                response.content.decode("utf-8"),
            )[1]
            html = re.split(f'<a href="/{year}/day/{day}| You can ', html)[0]
            print("".join(re.split("[<>]", html)[::2]))

        # if day == "all":
        #     for d in range(1, 26):
        #         if (year, d) in moduleDict:
        #             print(f"Day {d}:")
        #             result = run_day(year, d)
        #             print(f"{result[0]}\n{result[1]}\n")
        #     day = input(f"Run 20{year} day: ")
