cards = ''.join(str(i) for i in range(2, 10, 1)) + 'TJQKA'


def run(input_data: str):
    part1 = 0
    part2 = 0
    hands = []
    hands2 = []
    for i, line in enumerate(input_data.splitlines()):
        split = line.split()
        hand = split[0]
        bid = int(split[1])
        count_dict = {}
        for card in hand:
            if card in count_dict:
                count_dict[card] += 1
            else:
                count_dict[card] = 1
        count = list(count_dict.values())
        count.sort(reverse=True)
        hand_type = (count[0] - 1) * 2
        if count[0] <= 3 and count[1] == 2:
            hand_type += 1
        hand_values = [cards.index(c) + 2 for c in hand]
        hands.append((tuple(hand_values), bid, hand_type))

        for c, card in enumerate(hand):
            if card == 'J':
                hand_values[c] = 1
        if 'J' in count_dict and count[0] != 5:
            j_count = count_dict['J']
            i = 0 if j_count != count[0] else 1
            hand_type = (count[i] + j_count - 1) * 2
            if count[i] + j_count <= 3 and count[i + 1] >= 2:
                hand_type += 1
        hands2.append((tuple(hand_values), bid, hand_type))

    hands.sort(key=lambda h: (h[2], h[0]))
    for i, hand in enumerate(hands):
        part1 += hand[1] * (i + 1)
    hands2.sort(key=lambda h: (h[2], h[0]))
    for i, hand in enumerate(hands2):
        part2 += hand[1] * (i + 1)

    return part1, part2
