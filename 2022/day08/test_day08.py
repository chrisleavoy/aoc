from pathlib import Path


def read(filename: str) -> list[list[int]]:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return [list(map(int, line)) for line in f.read().splitlines(keepends=False)]


def visible(forest: list[list[int]]) -> int:
    n, m = len(forest), len(forest[0])
    total = 0
    total += len(forest) * 2  # top and bottom always visible
    total += len(forest[1:-1]) * 2  # left and right always visible
    found = [[0]*n for _ in forest]

    for i in range(1, n-1):
        last_max = forest[i][0]     # scan east
        for j in range(1, m-1):
            if forest[i][j] > last_max:
                last_max = forest[i][j]
                if not found[i][j]:
                    found[i][j] = 1
                    total += 1

        last_max = forest[i][m-1]     # scan west
        for j in range(m-1, 0, -1):
            if forest[i][j] > last_max:
                last_max = forest[i][j]
                if not found[i][j]:
                    found[i][j] = 1
                    total += 1

    for j in range(1, m-1):
        last_max = forest[0][j]  # scan south
        for i in range(1, n-1):
            if forest[i][j] > last_max:
                last_max = forest[i][j]
                if not found[i][j]:
                    found[i][j] = 1
                    total += 1

        last_max = forest[n-1][j]    # scan north
        for i in range(n-1, 0, -1):
            if forest[i][j] > last_max:
                last_max = forest[i][j]
                if not found[i][j]:
                    found[i][j] = 1
                    total += 1

    return total


def scenic_score(forest: list[list[int]]) -> int:
    size, max_score = len(forest), 0
    for i in range(size):
        for j in range(size):
            e, w, s, n = 0, 0, 0, 0  # east, west, south, noth
            for x in range(i+1, size):
                e += 1
                if forest[i][j] <= forest[x][j]:
                    break
            for x in range(i-1, -1, -1):
                w += 1
                if forest[i][j] <= forest[x][j]:
                    break
            for y in range(j+1, size):
                s += 1
                if forest[i][j] <= forest[i][y]:
                    break
            for y in range(j-1, -1, -1):
                n += 1
                if forest[i][j] <= forest[i][y]:
                    break
            max_score = max(max_score, e*w*s*n)
    return max_score


def test_sample():
    forest = read('day08-sample.txt')
    assert visible(forest) == 21
    assert scenic_score(forest) == 8


def test_sol1():
    forest = read('day08-input.txt')
    assert visible(forest) == 1719  # too high


def test_sol2():
    forest = read('day08-input.txt')
    assert scenic_score(forest) == 590824
