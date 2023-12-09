import datetime
import importlib.util
import os
import re
import requests

baseUrl = 'https://adventofcode.com/'

if __name__ == '__main__':
    now = datetime.datetime.now()
    year = now.year - 2001
    day = 25
    if now.month == 12:
        year += 1

    moduleDict = {}
    for filename in os.listdir(f'20{year}'):
        if filename[:2].isdecimal():
            d = int(filename[:2])
            if not 1 <= d <= 25:
                continue
            module_name = f'{year}{filename[:2]}'
            spec = importlib.util.spec_from_file_location(module_name, f'20{year}\\{filename}')
            module = importlib.util.module_from_spec(spec)
            moduleDict[year, d] = module
            spec.loader.exec_module(module)

            day = d

    sessionToken = open('sessionToken.txt').read()

    print(f'Run 20{year} day: {day}')
    while True:
        path = f'20{year}/{str(day).zfill(2)}.py'
        if not os.path.isfile(path) or os.stat(path).st_size == 0:
            template = open('template.py', 'r').read()
            open(path, 'a').write(template)
            break

        path = f'Inputs/{year}{str(day).zfill(2)}.txt'
        with open(path, 'a') as file:
            if os.stat(path).st_size == 0:
                response = requests.get(f'{baseUrl}20{year}/day/{day}/input',
                                        cookies={"session": sessionToken})
                file.write(response.content.decode("utf-8"))

        inputData = open(path, 'r').read()
        result = getattr(moduleDict[year, day], 'run')(inputData)
        print(f'{result[0]}\n{result[1]}')

        if input('Input \'y\' to submit: ') == 'y':
            part = 2 if result[1] != 0 else 1
            data = {
                'level': part,
                'answer': result[part - 1]
            }
            headers = {
                'User-Agent': 'Python 3.10',
                'From': 'trinhminhkhanh278@gmail.com'
            }
            response = requests.post(f'{baseUrl}20{year}/day/{day}/answer', data=data,
                                     cookies={"session": sessionToken},
                                     headers=headers)
            html = re.split(f'<main>\n<article><p>|</p></article>\n</main>', response.content.decode("utf-8"))[1]
            html = re.split(f'<a href=\"/{year}/day/{day}| You can ', html)[0]
            print(''.join(re.split('[<>]', html)[::2]))
        #     <a href=\"/20{year}/day/{day}

        day = input(f'Run 20{year} day: ')
        if day.isdecimal() and 1 <= int(day) <= 25:
            day = int(day)
        else:
            break
