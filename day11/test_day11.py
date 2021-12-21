from pathlib import Path


def read(filename: str):
    filename = Path(__file__).parent / filename
    data = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            data.append([int(x) for x in line.strip()])
    return data


def sol1(data, steps=100):
    flashes = 0
    for step in range(10000 if steps is None else steps):
        for i, _ in enumerate(data):
            for j, _ in enumerate(data[i]):
                data[i][j] += 1

        for i, _ in enumerate(data):
            for j, _ in enumerate(data[i]):
                if data[i][j] > 9:
                    flashes += 1
                    data[i][j] = 0
                    flashes += flash(data, i, j)

        if steps is None:
            if sum([sum(row) for row in data]) == 0:
                return 1+step
    return (data, flashes)


def flash(data, i, j):
    flashes = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            flashes += cascade(data, i+x, j+y)
    return flashes


def cascade(data, i, j):
    if i < 0 or i >= len(data):
        return 0
    if j < 0 or j >= len(data[i]):
        return 0
    if data[i][j] == 0:
        return 0

    flashes = 0
    data[i][j] += 1
    if data[i][j] > 9:
        flashes += 1
        data[i][j] = 0
        flashes += flash(data, i, j)

    return flashes


def sol2():
    result = 0
    return result


def test_base():
    assert sol1([], 0) == ([], 0)
    assert sol1([], 1) == ([], 0)
    assert sol1([[0]], 1) == ([[1]], 0)
    assert sol1([[9]], 1) == ([[0]], 1)
    assert sol1([[1]], 9) == ([[0]], 1)

    assert sol1([
        [1, 1, 1, 1, 1],
        [1, 9, 9, 9, 1],
        [1, 9, 1, 9, 1],
        [1, 9, 9, 9, 1],
        [1, 1, 1, 1, 1]
    ], 1) == ([
        [3, 4, 5, 4, 3],
        [4, 0, 0, 0, 4],
        [5, 0, 0, 0, 5],
        [4, 0, 0, 0, 4],
        [3, 4, 5, 4, 3]
    ], 9)


def test_sol1():
    _, flashes = sol1(read('day11-sample.txt'), 1)
    assert flashes == 0
    _, flashes = sol1(read('day11-sample.txt'), 2)
    assert flashes == 35

    _, flashes = sol1(read('day11-sample.txt'))
    assert flashes == 1656

    _, flashes = sol1(read('day11-input.txt'))
    assert flashes == 1627


def test_sol2():
    assert sol1(read('day11-sample.txt'), steps=None) == 195
    assert sol1(read('day11-input.txt'), steps=None) == 329
