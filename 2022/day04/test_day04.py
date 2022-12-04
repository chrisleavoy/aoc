import re
from pathlib import Path


def read(filename: str) -> list[str]:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return f.read().splitlines()


def points(line: str) -> (int, int, int, int):
    a, b, x, y = [int(x) for x in re.split("[,-]", line)]
    return a, b, x, y


def subset(a, b, x, y) -> bool:
    """ range [a-b] is a subset of range [x-y] or vice versa"""
    return a >= x and b <= y or a <= x and b >= y


def intersect(a, b, x, y) -> bool:
    """ range [a-b] intersects range [x-y] or vice versa"""
    return a <= x <= b or x <= a <= y or x <= b <= y


def test_sol1():
    lines = read('day04-input.txt')
    total = sum([subset(*points(line)) for line in lines])
    assert total == 498


def test_sol2():
    lines = read('day04-input.txt')
    total = sum([intersect(*points(line)) for line in lines])
    assert total == 859
