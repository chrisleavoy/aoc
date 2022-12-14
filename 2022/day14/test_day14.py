from pathlib import Path

Point = tuple[int, int]
Input = list[list[Point]]


def parse(line: str) -> list[Point]:
    return [tuple(map(int, p.split(','))) for p in line.split(' -> ')]


def read(filename: str) -> Input:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return [parse(line) for line in f.read().splitlines()]


def dump(rocks: set[Point], items: set[Point], origin: Point):
    print()
    x_min = min(p[0] for p in items)
    x_max = max(p[0] for p in items)
    y_min = 0
    y_max = max(p[1] for p in items)

    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if (x, y) in rocks:
                print('#', end='')
            elif (x, y) in items:
                print('o', end='')
            elif (x, y) == origin:
                print('+', end='')
            else:
                print('.', end='')
        print()


def solve(data: Input, floor=0, origin=(500, 0)) -> int:
    rocks = set[Point]()

    for points in data:
        pxa, pya = points[0]
        rocks.add((pxa, pya))
        for pxb, pyb in points[1:]:
            for pxc in range(pxb, pxa, -1 if pxb > pxa else 1):
                rocks.add((pxc, pyb))
            for pyc in range(pyb, pya, -1 if pyb > pya else 1):
                rocks.add((pxb, pyc))
            pxa, pya = pxb, pyb

    items = rocks.copy()

    dump(rocks, items, origin)

    abyss = max([rock[1] for rock in rocks])

    x, y = origin
    while True:
        if floor == 0 and y > abyss:
            break
        if floor != 0 and y >= abyss + floor - 1:
            items.add((x, y))
            x, y = origin
        elif (x, y+1) not in items:  # down
            y += +1
        elif (x-1, y+1) not in items:  # left
            x += -1
            y += 1
        elif (x+1, y+1) not in items:  # right
            x += +1
            y += 1
        else:
            items.add((x, y))
            if (x, y) == origin:
                break
            x, y = origin

    dump(rocks, items, origin)

    return len(items) - len(rocks)


def test_sample():
    assert parse('498,4 -> 498,6 -> 496,6') == [(498, 4), (498, 6), (496, 6)]
    segments = read('day14-sample.txt')
    assert solve(segments) == 24
    assert solve(segments, floor=2) == 93


def test_sol1():
    segments = read('day14-input.txt')
    assert solve(segments) == 961
    assert solve(segments, floor=2) == 26375
