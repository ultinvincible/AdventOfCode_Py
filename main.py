import datetime
import importlib.util
import os
import re
import time
import requests

base_url = "https://adventofcode.com/"


def run_day(year, day, measure_time=False):
    path = f"Inputs/{year}{str(day).zfill(2)}.txt"
    with open(path, "a") as file:
        if os.stat(path).st_size == 0:
            response = requests.get(
                f"{base_url}20{year}/day/{day}/input", cookies={"session": sessionToken}
            )
            file.write(response.content.decode("utf-8"))
    input_data = open(path, "r").read()
    run = getattr(moduleDict[year, day], "run")
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
    with open("sessionToken.py") as file:
        sessionToken = file.read()

    moduleDict = {}
    for filename in os.listdir(f"20{year}"):
        if filename[:2].isdecimal():
            d = int(filename[:2])
            if not 1 <= d <= 25:
                continue
            module_name = f"{year}{filename[:2]}"
            spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(f"20{year}", str(filename))
            )
            module = importlib.util.module_from_spec(spec)
            moduleDict[year, d] = module
            spec.loader.exec_module(module)

    day = max(moduleDict.keys())[1]

    print(f"Run 20{year} day: {day}")
    while True:
        path = f"20{year}/{str(day).zfill(2)}.py"
        if not os.path.isfile(path) or os.stat(path).st_size == 0:
            template = open("template.py", "r").read()
            open(path, "a").write(template)
            print("File created.")
            break

        result, runtime = run_day(year, day, True)
        print(f"{result[0]}\n{result[1]}\nRuntime: {round(runtime, 2)} s")

        if input("Input 'y' to submit: ") == "y":
            part = 2 if result[1] != 0 else 1
            data = {"level": part, "answer": result[part - 1]}
            headers = {
                "User-Agent": "Python 3.10",
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

        day = input(f"Run 20{year} day: ")
        if day == "all":
            for d in range(1, 26):
                if (year, d) in moduleDict:
                    print(f"Day {d}:")
                    result = run_day(year, d)
                    print(f"{result[0]}\n{result[1]}\n")
            day = input(f"Run 20{year} day: ")
        if day.isdecimal() and 1 <= int(day) <= 25:
            day = int(day)
        else:
            break
