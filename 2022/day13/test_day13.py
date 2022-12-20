from pathlib import Path
from functools import cmp_to_key


def read(filename: str) -> list:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return [list(map(eval, chunk.splitlines(keepends=False))) for chunk in f.read().split('\n\n')]


def compare(x, y):
    if isinstance(x, int) and isinstance(y, int):
        if x == y:
            return 0
        if x < y:
            return 1
        return -1

    for j in range(len(x)):
        if j >= len(y):
            return -1
        l = x[j]
        r = y[j]
        if isinstance(l, int) and isinstance(r, int):
            if l == r:
                continue
            if l < r:
                return 1
            return -1
        if isinstance(l, int):
            l = [l]
        elif isinstance(r, int):
            r = [r]

        result = compare(l, r)
        if result != 0:
            return result
    if len(x) == len(y):
        return 0
    return 1


def sol1(pairs):
    """find pairs in the right order"""
    pairs_in_order = []

    for i, pair in enumerate(pairs):
        in_order = compare(pair[0], pair[1])
        if in_order == 1:
            pairs_in_order.append(i+1)

    return sum(pairs_in_order)


def sol2(pairs):
    packets = [packet for pair in pairs for packet in pair]
    packets.append([[2]])
    packets.append([[6]])
    ordered = sorted(packets, key=cmp_to_key(compare), reverse=True)
    decorder_key = (ordered.index([[2]]) + 1) * (ordered.index([[6]]) + 1)
    return decorder_key


def test_sample():
    pairs = read('day13-sample.txt')
    assert sol1(pairs) == 13
    assert sol2(pairs) == 140


def test_sol1():
    pairs = read('day13-input.txt')
    assert sol1(pairs) == 6369


def test_sol2():
    pairs = read('day13-input.txt')
    assert sol2(pairs) == 25800
