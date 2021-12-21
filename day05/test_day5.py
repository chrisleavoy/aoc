from pathlib import Path
import re


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def points(self):
        return (self.x1, self.y1, self.x2, self.y2)

    def __repr__(self) -> str:
        return f'({self.x1},{self.y1} -> {self.x2},{self.y2})'


class Vents:
    def read(filename: str):
        filename = Path(__file__).parent / filename
        s = Vents()
        with open(filename, encoding='utf-8') as f:
            content = f.read()
        s.data = []
        for line in content.splitlines():
            l = re.split(',| -> ', line)
            s.data.append(Line(*l))
        return s

    def solution(self, size: int, skip_horizontal: bool):
        # fill NxN matrix with 0
        grid = [[0]*size for _ in range(size)]
        # count of cells w/ 2 or more overlapping lines
        count = 0
        for line in self.data:
            x1, y1, x2, y2 = line.points()
            xv = -1 if x1 > x2 else 0 if x1 == x2 else 1
            yv = -1 if y1 > y2 else 0 if y1 == y2 else 1

            if xv != 0 and yv != 0:
                if skip_horizontal:
                    continue
                for x, y in zip(range(x1, x2 + xv, xv), range(y1, y2 + yv, yv)):
                    grid[y][x] += 1
                    if grid[y][x] == 2:
                        count += 1
            elif xv != 0:
                for x in range(x1, x2 + xv, xv):
                    grid[y1][x] += 1
                    if grid[y1][x] == 2:
                        count += 1
            elif yv != 0:
                for y in range(y1, y2 + yv, yv):
                    grid[y][x1] += 1
                    if grid[y][x1] == 2:
                        count += 1
            else:
                print(line)
                raise ValueError('oops')

        return count

    def __repr__(self):
        return f'{self.data}'


def test_1():
    # print(Vents.read('day5-sample.txt'))
    assert Vents.read('day5-sample.txt').solution(10, True) == 5
    assert Vents.read('day5-input.txt').solution(1000, True) == 7142


def test_2():
    assert Vents.read('day5-sample.txt').solution(10, False) == 12
    assert Vents.read('day5-input.txt').solution(1000, False) == 20012
