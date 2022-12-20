from pathlib import Path
import re


class Input():
    def __init__(self, nums, cards, size):
        self.nums = nums
        self.cards = cards
        self.size = size

    @classmethod
    def read(cls, filename: str):
        path = Path(__file__).parent.joinpath(filename)
        with open(path, encoding='utf-8') as f:
            nums = [int(x) for x in f.readline().strip().split(',')]
            f.readline()
            cards = []
            card = []
            for line in f:
                line = line.strip()
                if line == '':
                    cards.append(card)
                    card = []
                else:
                    v = [int(x) for x in re.split(' +', line)]
                    card.append(v)
            cards.append(card)

            # num of rows/cols:
            size = len(cards[0])

            return Input(nums, cards, size)

    def __str__(self):
        return f'nums={self.nums}, cards={self.cards}'


def read(filename: str) -> Input:
    return Input.read(filename)


def fn1(inputs):
    num, card = winner(inputs)

    # sum remaining unmarked numbers on that board
    result = 0
    for i in range(inputs.size):
        for j in range(inputs.size):
            if card[i][j] != -1:
                result += card[i][j]

    return num * result


def winner(inputs):
    for num in inputs.nums:
        for card in inputs.cards:
            for i in range(inputs.size):
                for j in range(inputs.size):
                    if card[i][j] == num:
                        # mark the number (set to -1)
                        card[i][j] = -1
                        # winner if sum of row or col == -size
                        if sum([card[x][j] for x in range(inputs.size)]) == -inputs.size:
                            return (num, card)
                        elif sum([card[i][x] for x in range(inputs.size)]) == -inputs.size:
                            return (num, card)

    raise ValueError('no winner found')


def loser(inputs):
    # card indexes that have not yet won:
    cards = list(range(len(inputs.cards)))
    for num in inputs.nums:
        # copy the card indexes so that we can iterate while removing
        for c in list(cards):
            card = inputs.cards[c]
            for i in range(inputs.size):
                for j in range(inputs.size):
                    if card[i][j] == num:
                        # mark the number (set to -1)
                        card[i][j] = -1
                        # winner if sum of row or col == -size
                        if sum([card[x][j] for x in range(inputs.size)]) == -inputs.size:
                            # eliminate card
                            cards.remove(c)
                            if len(cards) == 0:
                                return (num, card)
                        elif sum([card[i][x] for x in range(inputs.size)]) == -inputs.size:
                            # eliminate card
                            cards.remove(c)
                            if len(cards) == 0:
                                return (num, card)
    raise ValueError('no loser found')


def fn2(inputs):
    num, card = loser(inputs)

    # sum remaining unmarked numbers on that board
    result = 0
    for i in range(inputs.size):
        for j in range(inputs.size):
            if card[i][j] != -1:
                result += card[i][j]

    return num * result


def test_1():
    # print(inputs('day4-sample.txt'))
    assert fn1(read('day4-sample.txt')) == 4512


def test_2():
    # print(inputs('day2-part1-input.txt'))
    assert fn2(read('day4-sample.txt')) == 1924
    assert fn2(read('day4-input.txt')) == 7075
