import csv
import datetime
import importlib.util
import os
import re
import sys
import time
import traceback
from typing import Callable

import requests

from config import SESSION_TOKEN as session_token

base_url = "https://adventofcode.com/"
with open("answers", newline="") as file:
    reader = csv.DictReader(file)
    answers = {
        (int(row["year"]), int(row["day"])): (row["part1"], row["part2"])
        for row in reader
    }


def run_day(year: int, day: int, measure_time=True):
    if module := sys.modules.get(f"20{year}.{day:02}", None):
        importlib.reload(module)
    elif os.path.exists(year_path := f"20{year}"):
        listdir = os.listdir(year_path)
        if files := [
            filename for filename in listdir if filename[:2] == "{:02}".format(day)
        ]:
            module = importlib.import_module(f"{year_path}.{files[0][:-3]}")
    if not module:
        raise FileNotFoundError("File not found.")
    try:
        run: Callable[[str], tuple[str, str]] = getattr(module, "run", None)
    except AttributeError:
        raise AttributeError("Module does not have a 'run' method.")

    if not os.path.exists(input_path := "Inputs"):
        os.mkdir(input_path)
    input_path = os.path.join(input_path, f"{year}{day:02}.txt")
    if not os.path.isfile(input_path) or os.stat(input_path).st_size == 0:
        # Minimize requests
        # https://www.reddit.com/r/adventofcode/comments/3v64sb/
        response = requests.get(
            f"{base_url}20{year}/day/{day}/input",
            cookies={"session": session_token},
        )
        response.raise_for_status()
        with open(input_path, "w") as file:
            file.write(response.content.decode())
    with open(input_path) as file:
        input_data = file.read()

    start = time.time()
    result = run(input_data)
    end = time.time()
    answer = answers.get((year, day), None)
    for i in (0, 1):
        if result[i]:
            multiline = "\n" in (part := str(result[i]))
            if i == 1 and multiline:
                print()
            print(part.ljust(20), end="| " if not multiline else "\n")
            print(
                (
                    "Correct"
                    if part == answer[i]
                    else f"Incorrect{': ' if not multiline else '\n'}{answer[i]}"
                )
                if answer and answer[i]
                else "No answer"
            )
        else:
            print("Not implemented.")
    if measure_time and any(result):
        print(f"Runtime: {round(end - start, 3)} s.")
    return result


def submit(year: int, day: int, result: tuple[str, str]):
    # Requested by the AoC creator at:
    # https://www.reddit.com/r/adventofcode/comments/z9dhtd/
    headers = {
        "User-Agent": "github.com/ultinvincible/AdventOfCode_Py by trinhminhkhanh278@gmail.com",
    }

    part = 2 if result[1] else 1
    data = {"level": part, "answer": result[part - 1]}
    # Minimize requests
    response = requests.post(
        f"{base_url}20{year}/day/{day}/answer",
        data=data,
        cookies={"session": session_token},
        headers=headers,
    )
    response.raise_for_status()

    main = re.split(
        r"<main>\n<article><p>|</p></article>\n</main>",
        response.content.decode(),
    )[1]
    html = re.split(r"\[| You can ", main)[0]
    message = "".join(re.split("[<>]", html)[::2])
    # print(main)
    print(*message.split(), sep=" ")

    if part == 2 and re.split("[!.]", message, 1)[0] in (
        "That's the right answer",
        "You don't seem to be solving the right level",
    ):
        with open("answers", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([year, day, *result])
            answers[year, day] = str(result[0]), str(result[1])


if __name__ == "__main__":
    today = datetime.datetime.today()
    year = today.year - 2001
    if today.month == 12:
        year += 1
    day = 1

    result = (None,)
    while True:
        prompt = f"Run [year]{{day}} ({year}{day:02}| {day:>2}| all)"
        if any(result):
            prompt += " or 's' to submit"
        command = input(prompt + ": ")

        if command == "s":
            if any(result) and not answers[year, day]:
                submit(year, day, result)
                result = (None,)
            else:
                print("There is no result to submit.")
            continue

        if command == "all":
            for d in range(1, 26):
                print(f"---- Day {d:02} ----")
                try:
                    run_day(year, d)
                except Exception as e:
                    print(type(e), e)
            continue

        try:
            assert 1 <= (input_day := int(command[-2:])) <= 25
            if len(command) > 2:
                assert 15 <= (input_year := int(command[:-2])) <= today.year - 2000
                year = input_year
            day = input_day
        except (IndexError, ValueError, AssertionError):
            print("Invalid options provided. Exiting.")
            break

        path = f"20{year}"
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, f"{day:02}.py")
        if not os.path.isfile(path) or os.stat(path).st_size == 0:
            with open("template.py") as template, open(path, "w") as file:
                file.write(template.read())
            print("File created.")
            continue

        try:
            result = run_day(year, day)
        except Exception:
            traceback.print_exc()
