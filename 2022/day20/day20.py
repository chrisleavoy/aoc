import unittest
from collections import deque
from pathlib import Path


def read(filename: str) -> list[int]:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return list(map(int, f.read().splitlines()))


def solve(filename: str, key=1, count=1):
    nums = read(filename)
    data = deque(enumerate((num * key for num in nums)))

    for _ in range(count):
        for idx in range(len(data)):
            while data[0][0] != idx:
                data.rotate(-1)

            ord_n, n_shift = data.popleft()
            data.rotate(-1 * n_shift)
            data.appendleft((ord_n, n_shift))

    while data[0][1] != 0:
        data.rotate(-1)

    coord = []
    for _ in range(3):
        for _ in range(1000):
            data.rotate(-1)
        coord.append(data[0][1])
    return sum(coord)


if __name__ == '__main__':
    tc = unittest.TestCase()
    tc.assertEqual(solve('day20-sample.txt'), 3)
    tc.assertEqual(solve('day20-sample.txt', 811589153, 10), 1623178306)

    tc.assertEqual(solve('day20-input.txt'), 11616)
    tc.assertEqual(solve('day20-input.txt', 811589153, 10), 9937909178485)
