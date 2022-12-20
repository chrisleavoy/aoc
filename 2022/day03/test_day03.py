import unittest
from itertools import zip_longest
from pathlib import Path


def read(filename: str) -> list[str]:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return f.read().splitlines()


def item_priority(ch: str) -> int:
    priority = ord(ch) - ord('A') + 27
    if priority > 52:
        priority -= 58
    return priority


def common_item_priority(s: str) -> int:
    """Given a string s, return the priority of the character that appears in both the first and second half.
    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52."""
    n = len(s)
    common = set(s[0:n // 2]) & set(s[n // 2:])
    assert len(common) == 1
    ch = common.pop()
    return item_priority(ch)


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def group_common_item_priority(group: list[str]) -> int:
    assert len(group) == 3
    common = set(group[0]) & set(group[1]) & set(group[2])
    assert len(common) == 1
    ch = common.pop()
    return item_priority(ch)


class TestDay03(unittest.TestCase):
    def test_sample(self):
        lines = read('day03-sample.txt')
        self.assertEqual(common_item_priority('vJrwpWtwJgWrhcsFMMfFFhFp'), 16)
        total = sum([common_item_priority(s) for s in lines])
        self.assertEqual(total, 157)

        total2 = sum([group_common_item_priority(group)
                     for group in grouper(3, lines)])
        self.assertEqual(total2, 70)

    def test_sol1(self):
        total = sum([common_item_priority(s) for s in read('day03-input.txt')])
        self.assertEqual(total, 0)

    def test_sol2(self):
        lines = read('day03-input.txt')
        total = sum([group_common_item_priority(group)
                    for group in grouper(3, lines)])
        self.assertEqual(total, 2790)


if __name__ == '__main__':
    unittest.main()
