import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Monkey:
    items: list[int]  # worry level of items
    op: (str, any)
    divisor: int  # test for determining next monkey
    next: (int, int)  # next monkey on False, True
    inspected: int = 0  # count of items inspected over rounds


def read(filename: str) -> list[Monkey]:
    monkeys = []
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        lines = f.read().splitlines(keepends=False)
        for i in range(0, len(lines), 7):
            items = list(map(int, lines[i + 1][18:].split(', ')))
            operation = lines[i + 2][19:].split(' ')
            if operation[2] != 'old':
                operation[2] = int(operation[2])
            divisor = int(lines[i + 3][21:])
            t = int(lines[i + 4][29:])
            f = int(lines[i + 5][29:])
            m = Monkey(items, operation, divisor, (f, t))
            monkeys.append(m)

        return monkeys


def sol(monkeys: list[Monkey], rounds=20):
    # python wll cry doing math on huge numbers as worry levels rise
    # so, we reduce the big numbers by the product of all divisors
    reducer = math.prod([m.divisor for m in monkeys])

    for r in range(rounds):
        for m in monkeys:
            # on its turn, a monkey throws all its items
            items = m.items
            m.items = []
            for item in items:
                m.inspected += 1

                v = item if m.op[2] == 'old' else m.op[2]
                if m.op[1] == "*":
                    item *= v
                elif m.op[1] == "+":
                    item += v

                if rounds == 20:
                    item = item // 3

                item = item % reducer
                n = m.next[1 if item % m.divisor == 0 else 0]
                monkeys[n].items.append(item)

    inspected = sorted([m.inspected for m in monkeys])
    return inspected[-1] * inspected[-2]


def test_sample():
    monkeys = read('day11-sample.txt')
    assert sol(monkeys) == 10605
    monkeys = read('day11-sample.txt')
    assert sol(monkeys, rounds=10_000) == 2713310158


def test_sol1():
    monkeys = read('day11-input.txt')
    assert sol(monkeys) == 108240
    monkeys = read('day11-input.txt')
    assert sol(monkeys, rounds=10_000) == 25712998901
