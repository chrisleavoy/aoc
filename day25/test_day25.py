
from copy import deepcopy
from pathlib import Path

P, E, S = '.', '>', 'v'


class Puzzle:
    def __init__(self, s) -> None:
        if isinstance(s, list):
            self.grid = s
            self.steps = 0
        else:
            filename = Path(__file__).parent/s
            self.grid = []
            self.steps = 0
            with open(filename, encoding='utf-8') as f:
                for line in f.read().splitlines():
                    self.grid.append(list(line))

    def resolve(self, max_steps=100_000):
        mutated = True
        N = len(self.grid[0])
        M = len(self.grid)
        while mutated and self.steps < max_steps:
            mutated = False
            grid = deepcopy(self.grid)
            for r, row in enumerate(self.grid):
                for c, cell in enumerate(row, -1):
                    if cell == P and row[c % N] == E:
                        grid[r][c % N] = P
                        grid[r][c + 1] = E
                        mutated = True
            self.grid = grid
            grid = deepcopy(self.grid)
            for c in range(N):
                for r in range(-1, M-1):
                    cell = self.grid[r+1][c]
                    if cell == P and self.grid[r % M][c] == S:
                        grid[r % M][c] = P
                        grid[r + 1][c] = S
                        mutated = True
            self.steps += 1
            self.grid = grid
        return self


def test_simple():
    p = Puzzle('day25-simple.txt').resolve()
    assert p.steps == 3


def test_simple2():
    p = Puzzle('day25-simple2.txt').resolve()
    assert p.steps == 3


def test_edges():
    assert Puzzle([
        [E, E, P],
        [P, P, P],
        [P, P, P],
    ]).resolve(1).grid == [
        [E, P, E],
        [P, P, P],
        [P, P, P],
    ]
    assert Puzzle([
        [S, P, P],
        [S, P, P],
        [P, P, P],
    ]).resolve(1).grid == [
        [S, P, P],
        [P, P, P],
        [S, P, P],
    ]
    assert Puzzle([
        [E, S, P],
        [P, P, P],
        [P, P, P],
    ]).resolve(1).grid == [
        [E, P, P],
        [P, S, P],
        [P, P, P],
    ]
    assert Puzzle([
        [P, S, P],
        [E, P, P],
        [P, P, P],
    ]).resolve(1).grid == [
        [P, S, P],
        [P, E, P],
        [P, P, P],
    ]
    assert Puzzle([
        [P, P, P],
        [P, P, P],
        [S, P, E],
    ]).resolve(1).grid == [
        [S, P, P],
        [P, P, P],
        [P, P, E],
    ]


def test_sample():
    p = Puzzle('day25-sample.txt').resolve()
    assert p.steps == 58


def test_input():
    p = Puzzle('day25-input.txt').resolve()
    assert p.steps == 571
