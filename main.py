import datetime
import importlib.util
import os
import re
import sys
import time
import traceback

import requests

from config import SESSION_TOKEN as session_token

base_url = "https://adventofcode.com/"


def run_day(year: int, day: int, measure_time=True):
    if module := sys.modules.get(f"20{year}.{day:02}", None):
        importlib.reload(module)
    else:
        year_path = f"20{year}"
        if os.path.exists(year_path):
            listdir = os.listdir(year_path)
            if files := [
                filename for filename in listdir if filename[:2] == "{:02}".format(day)
            ]:
                module = importlib.import_module(f"{year_path}.{files[0][:-3]}")
    if not module:
        raise FileNotFoundError("File not found.")
    if not (run := getattr(module, "run", None)):
        raise AttributeError("Module does not have a 'run' method.")

    if not os.path.exists(input_path := "Inputs"):
        os.mkdir(input_path)
    input_path = os.path.join(input_path, f"{year}{day:02}.txt")
    if not os.path.isfile(input_path) or os.stat(input_path).st_size == 0:
        with open(input_path, "w") as file:
            # Minimize requests
            # https://www.reddit.com/r/adventofcode/comments/3v64sb/
            response = requests.get(
                f"{base_url}20{year}/day/{day}/input",
                cookies={"session": session_token},
            )
            file.write(response.content.decode("utf-8"))
    with open(input_path, "r") as file:
        input_data = file.read()

    if measure_time:
        start = time.time()
    result = run(input_data)
    if measure_time:
        end = time.time()
    print(f"{result[0] or 'Not implemented.'}\n{result[1] or 'Not implemented.'}")
    if measure_time and any(result):
        print(f"Runtime: {round(end-start, 3)} s.")
    #     return result, end-start
    # return result


def submit(year: int, day: int, result: tuple[str, str]):
    # Requested by the AoC creator at:
    # https://www.reddit.com/r/adventofcode/comments/z9dhtd/
    headers = {
        "User-Agent": "github.com/ultinvincible/AdventOfCode_Py by trinhminhkhanh278@gmail.com",
    }

    part = 2 if result[1] else 1
    data = {"level": part, "answer": result[part - 1]}
    response = requests.post(
        f"{base_url}20{year}/day/{day}/answer",
        data=data,
        cookies={"session": session_token},
        headers=headers,
    )
    main = re.split(
        "<main>\n<article><p>|</p></article>\n</main>",
        response.content.decode(),
    )[1]
    html = re.split(f'<a href="/{year}/day/{day}| You can ', main)[0]
    message = "".join(re.split("[<>]", html)[::2])
    print(main)
    print(message)


if __name__ == "__main__":
    today = datetime.datetime.today()
    year = today.year - 2001
    if today.month == 12:
        year += 1
    day = 1

    result = (None,)
    while True:
        prompt = f"Run [year] day ({year} {day:02}|{day}|all)"
        if any(result):
            prompt += " or 's' to submit"
        options = input(prompt + ": ").split()

        if options == ["s"]:
            submit(year, day, result)
            result = (None,)
            continue

        if options == ["all"]:
            for d in range(1, 26):
                print(f"---- Day {d:02} ----")
                run_day(year, d)
            continue

        try:
            assert 1 <= (day := int(options[-1])) <= 25
            if (
                len(options) > 1
                and 15 <= (option_year := int(options[0])) <= today.year - 2000
            ):
                year = option_year
        except (IndexError, ValueError, AssertionError):
            print("Invalid options provided. Exiting.")
            break

        path = f"20{year}"
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, f"{day:02}.py")
        if not os.path.isfile(path) or os.stat(path).st_size == 0:
            with open("template.py", "r") as file:
                template = file.read()
            with open(path, "w") as file:
                file.write(template)
            print("File created.")
            continue

        try:
            run_day(year, day)
        except Exception:
            traceback.print_exc()
