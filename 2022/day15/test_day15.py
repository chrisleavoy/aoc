from pathlib import Path
from itertools import combinations, pairwise
import re

Point = tuple[int, int]
Input = list[list[Point]]


def parse(line: str) -> list[Point]:
    r = re.compile(
        r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

    m = r.match(line)
    if m is None:
        raise ValueError(f'{line=}')

    g = list(map(int, m.groups()))
    return [(g[0], g[1]), (g[2], g[3])]


def read(filename: str) -> Input:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return [parse(line) for line in f.read().splitlines()]


def read2(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return f.read()


S, B, V = 'S', 'B', '#'


def manhattan_dist(s: Point, b: Point) -> int:
    return abs(s[0] - b[0]) + abs(s[1] - b[1])


def dump(items: dict[Point, str]):
    print()
    x_min = min(p[0] for p in items)
    x_max = max(p[0] for p in items)
    y_min = min(p[1] for p in items)
    y_max = max(p[1] for p in items)

    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if (x, y) in items:
                print(items[(x, y)], end='')
            else:
                print('.', end='')
        print()


def solve(data: Input, row=10) -> int:
    items = dict[Point, str]()
    count = 0
    for sensor, beacon in data:
        # sensor = (8, 7)
        # beacon = (2, 10)
        dist_sensor_row = abs(sensor[1] - row)
        sensor_range = manhattan_dist(sensor, beacon)

        if dist_sensor_row > sensor_range:
            continue

        # items[sensor], items[beacon] = S, B
        if sensor[1] == row:
            items[sensor] = S
        if beacon[1] == row:
            items[beacon] = B

        dxmin = -sensor_range + dist_sensor_row
        dxmax = +sensor_range - dist_sensor_row
        for dx in range(dxmin, dxmax + 1):
            p = (sensor[0] + dx, row)
            if p not in items:
                items[p] = V
                count += 1
        # break

        # dyr = 0
        # for dx in range(-dist-1, dist+1):
        #     for dy in range(-dyr+1, dyr):
        #         p = (sensor[0] + dx, sensor[1] + dy)
        #         if p[1] != y:
        #             continue
        #         if p not in items:
        #             items[p] = V
        #             count += 1
        #     dyr += 1 if dx < 0 else -1

    # dump(items)
    if row % 10 == 1:
        n = len(items)
        minx = min([p[0] for p in items])
        maxx = max([p[0] for p in items])
        for x in range(minx, maxx+1):
            if (x, row) not in items:
                return tuning_freq((x, row))

    return count


def tuning_freq(p: Point) -> int:
    return p[0]*4_000_000 + p[1]


def test_parse():
    line = 'Sensor at x=2, y=18: closest beacon is at x=-2, y=15'
    assert parse(line) == [(2, 18), (-2, 15)]


def test_sample():
    data = read('day15-sample.txt')
    assert solve(data) == 26
    s = read2('day15-sample.txt')
    assert solve2(s) == 56000011


def test_sol1():
    data = read('day15-input.txt')
    assert solve(data, row=2000000) == 5525990
    s = read2('day15-input.txt')
    assert solve2(s) == 11756174628223


def line_intersection(line1, line2):
    xdiff = complex(line1[0].real - line1[1].real,
                    line2[0].real - line2[1].real)
    ydiff = complex(line1[0].imag - line1[1].imag,
                    line2[0].imag - line2[1].imag)

    def det(a, b):
        return a.real * b.imag - a.imag * b.real

    div = det(xdiff, ydiff)
    if div == 0:
        # lines do not intersect
        return False

    d = complex(det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return complex(x, y)


def mh_dist(a, b):
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def solve2(inp):
    inp = inp.splitlines()
    radii = {}
    for line in inp:
        sensor, beacon = line[10:].split(":")
        beacon = beacon.split(" at ")[1]
        sensor = complex(*[int(x.split("=")[1]) for x in sensor.split(", ")])
        beacon = complex(*[int(x.split("=")[1]) for x in beacon.split(", ")])
        radii[sensor] = mh_dist(sensor, beacon)

    pairs = []
    for (s1, d1), (s2, d2) in combinations(radii.items(), 2):
        if mh_dist(s1, s2) == d1 + d2 + 2:
            pairs.append((s1, s2))

    for (s1, s2), (s3, s4) in combinations(pairs, 2):
        #        ##S##
        #         ###d#
        #          #d#S#
        #             #
        # basic idea: find the diagonals ("d" in the drawing above) between 2 adjacent sensor circles
        # (adjacent = seperated by a line of width 1)
        # compute the intersection of the diagonals for all pairs of pairs of adjacent sensor border circles
        # if it exists, it must contain a beacon, but it can’t be a known beacon because then its sensor would have to be on top of it
        s1, s2 = sorted([s1, s2], key=lambda s: s.real)
        s3, s4 = sorted([s3, s4], key=lambda s: s.real)
        diags = []
        for sensor_a, sensor_b in zip([s1, s3], [s2, s4]):
            r_a = radii[sensor_a] + 1
            r_b = radii[sensor_b] + 1
            end = complex(sensor_a.real + r_a, sensor_a.imag)
            start = complex(sensor_b.real - r_b, sensor_b.imag)
            diags.append([start, end])

        b = line_intersection(diags[0], diags[1])
        if b is not False:
            return int(round(b.real) * 4000000 + round(b.imag))
