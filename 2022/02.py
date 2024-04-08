def run(input_data: str):
    guide = [
        (ord(line[0]) - ord("A"), ord(line[2]) - ord("X"))
        for line in input_data.splitlines()
    ]
    return sum(
        [
            eachRound[1] + 1 + (eachRound[1] - eachRound[0] + 1) % 3 * 3
            for eachRound in guide
        ]
    ), sum(
        [
            (eachRound[0] + eachRound[1] + 2) % 3 + 1 + eachRound[1] * 3
            for eachRound in guide
        ]
    )
