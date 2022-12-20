from pathlib import Path

PADDING = 2
COLPAD = '00'


class Puzzle:
    def __init__(self, filename: str):
        path = Path(__file__).parent.joinpath(filename)
        self.filename = filename
        t = str.maketrans('.#', '01')

        with open(self.filename, encoding='utf-8') as f:
            lines = f.read().splitlines()
            self.algorithm = lines[0].translate(t)
            rows = len(lines[2:])+PADDING*2
            cols = len(lines[2])+PADDING*2
            self.grid = [None]*rows
            for i in range(PADDING):
                self.grid[i] = '0'*cols
                self.grid[rows-1-i] = '0'*cols
            for i, line in enumerate(lines[2:]):
                self.grid[PADDING+i] = COLPAD + line.translate(t) + COLPAD

    def resolve(self, s: str):
        ''' returns 1 or 0 '''
        d = int(s, 2)
        return self.algorithm[d]

    def apply(self, steps=1):
        for _ in range(steps):
            b = self.resolve(self.grid[0][0:9])
            rows = len(self.grid)+PADDING
            cols = len(self.grid[0])+PADDING
            output = [None]*rows
            for i in range(PADDING):
                output[i] = b*cols
                output[rows-1-i] = b*cols
            for i in range(1, len(self.grid) - 1):
                v = ''
                for j in range(1, len(self.grid[0]) - 1):
                    v += self.resolve(self.grid[i-1][j-1: j+2] +
                                      self.grid[i-0][j-1: j+2] +
                                      self.grid[i+1][j-1: j+2])
                output[i+1] = b*2 + v + b*2
            self.grid = output

    def count(self):
        return sum([row.count('1') for row in self.grid])


def test_sample():
    assert int('000100010', 2) == 34
    p = Puzzle('day20-sample.txt')
    assert p.algorithm[0] == '0'
    assert p.algorithm[34] == '1'
    p.apply(2)
    assert p.count() == 35
    p.apply(48)
    assert p.count() == 3351


def test_input():
    p = Puzzle('day20-input.txt')
    assert p.algorithm[0] == '1'  # sneaky bugger!
    p.apply(2)
    assert p.count() == 5395
    p.apply(48)
    assert p.count() == 17584
