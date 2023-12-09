import helper

class y2022:
    debug = 0

    def d01(self, path):
        sections = open(path).read().split('\n\n')
        elves = [sum([int(calories) for calories in sect.split('\n') if calories != ''])
                 for sect in sections]
        elves.sort()
        return elves[-1], elves[-1] + elves[-2] + elves[-3]

    def d02(self, path):
        guide = [(ord(line[0]) - ord('A'), ord(line[2]) - ord('X'))
                 for line in open(path) if line != '\n']
        return sum([eachRound[1] + 1 + (eachRound[1] - eachRound[0] + 1) % 3 * 3 for eachRound in guide]), \
            sum([(eachRound[0] + eachRound[1] + 2) % 3 + 1 + eachRound[1] * 3 for eachRound in guide])

    def d03(self, path):
        def priority(char):
            return ord(char) - ord('A') + 27 if ord(char) < ord('a') else ord(char) - ord('a') + 1

        rucksacks = [line.strip('\n') for line in open(path)]
        sum1 = 0
        for rs in rucksacks:
            for item in rs[:len(rs) // 2]:
                if item in rs[len(rs) // 2:]:
                    sum1 += priority(item)
                    if self.debug == 1:
                        print(priority(item))
                    break
        sum2 = 0
        for r in range(len(rucksacks))[::3]:
            for item in rucksacks[r]:
                if item in rucksacks[r + 1] and item in rucksacks[r + 2]:
                    sum2 += priority(item)
                    break
        return sum1, sum2

    def d04(self, path):
        pairs = [[int(value) for value in line.replace(',', '-').split('-')] for line in open(path)]
        sum1 = 0
        for pair in pairs:
            if (pair[0] - pair[2]) * (pair[1] - pair[3]) <= 0:
                sum1 += 1
        sum2 = 0
        for pair in pairs:
            if pair[1] >= pair[2] and pair[3] >= pair[0]:
                sum2 += 1
        return sum1, sum2
