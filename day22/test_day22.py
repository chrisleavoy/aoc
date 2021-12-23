import re
from pathlib import Path
from bitarray import bitarray


def volume(x1, x2, y1, y2, z1, z2):
    return (x2 + 1 - x1) * (y2 + 1 - y1) * (z2 + 1 - z1)


class Puzzle:
    def __init__(self, filename: str):
        filename = Path(__file__).parent / filename
        # reboot steps: [toggle, x1, x2, y1, y2, z1, z2]
        self.cuboids = []
        self.grid = []
        self.cubes = []

        with open(filename, encoding='utf-8') as f:
            for line in f.read().splitlines():
                tokens = re.split(' x=|,[yz]=|[.]{2}', line)
                tokens = [int(t if t[0] != 'o' else t[1] == 'n')
                          for t in tokens]
                self.cuboids.append(tokens)

    def reboot(self):
        s, n = 50, 51 - -50  # c-50..c50 -> 0..c100 (len=101)
        grid = [[largearray(n) for _ in range(n)] for _ in range(n)]
        for cuboid in self.cuboids:
            toggle, x1, x2, y1, y2, z1, z2 = cuboid
            for x in range(max(x1+s, 0), min(x2+s, n)+1):
                for y in range(max(y1+s, 0), min(y2+s, n)+1):
                    # assert z1 == min(z1, z2) and z2 == max(z1, z2)
                    # for z in range(max(z1+50, 0), min(z2+50, n)+1):
                    #     grid[x][y][z] = toggle
                    f1 = max(z1+s, 0)
                    f2 = min(z2+s, n) + 1
                    if f1 < n and f2 > 0:
                        grid[x][y][f1:f2] = toggle
        self.grid = grid
        return self

    def solve(self):
        cubes = set()
        # assumption: p1 is less than p2 for all x,y,z
        for toggle, x1, x2, y1, y2, z1, z2 in self.cuboids:
            for xc1, xc2, yc1, yc2, zc1, zc2 in set(cubes):
                xi1, xi2 = max(x1, xc1), min(x2, xc2)
                yi1, yi2 = max(y1, yc1), min(y2, yc2)
                zi1, zi2 = max(z1, zc1), min(z2, zc2)
                if xi1 <= xi2 and yi1 <= yi2 and zi1 <= zi2:
                    cubes.discard((xc1, xc2, yc1, yc2, zc1, zc2))
                    if xc1 <= xi1 <= xc2:
                        cubes.add((xc1, xi1 - 1, yc1, yc2, zc1, zc2))
                        xc1 = xi1
                    if xc1 <= xi2 <= xc2:
                        cubes.add((xi2 + 1, xc2, yc1, yc2, zc1, zc2))
                        xc2 = xi2
                    if yc1 <= yi1 <= yc2:
                        cubes.add((xc1, xc2, yc1, yi1 - 1, zc1, zc2))
                        yc1 = yi1
                    if yc1 <= yi2 <= yc2:
                        cubes.add((xc1, xc2, yi2 + 1, yc2, zc1, zc2))
                        yc2 = yi2
                    if zc1 <= zi1 <= zc2:
                        cubes.add((xc1, xc2, yc1, yc2, zc1, zi1 - 1))
                        zc1 = zi1
                    if zc1 <= zi2 <= zc2:
                        cubes.add((xc1, xc2, yc1, yc2, zi2 + 1, zc2))
                        zc2 = zi2
            if toggle:
                cubes.add((x1, x2, y1, y2, z1, z2))
            self.cubes = cubes
        return self

    def sum(self):
        n = 51 - -50
        return sum([sum([self.grid[x][y].count(1) for x in range(n)]) for y in range(n)])

    def sum_cubes(self):
        return sum(volume(*cube) for cube in self.cubes)


def test_sample():
    p = Puzzle('day22-sample.txt')
    assert p.reboot().sum() == 590784
    assert p.solve().sum_cubes() == 39769202357779


def test_input():
    p = Puzzle('day22-input.txt')
    assert p.reboot().sum() == 580810
    assert p.solve().sum_cubes() == 1265621119006734


def test_larger():
    p = Puzzle('day22-larger.txt')
    assert p.reboot().sum() == 474140
    assert p.solve().sum_cubes() == 2758514936282235


def largearray(n):
    a = bitarray(n)
    a.setall(0)
    return a


def test_bitarray():
    a = bitarray(2**15)  # 32kb
    a.setall(0)
    print(len(a))
    print(f'0s: {a.count(0)}')
    print(f'1s: {a.count(1)}')
    a[1414:] = True
    print(f'0s: {a.count(0)}')
    print(f'1s: {a.count(1)}')
