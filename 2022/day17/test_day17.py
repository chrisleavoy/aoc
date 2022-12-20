from itertools import cycle
from pathlib import Path


def read(filename: str) -> list[int]:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return [1 if jet_dir == '>' else -1 for jet_dir in f.readline().strip()]


class Shape:
    def __init__(self, points: list[tuple[int, int]]):
        self.points = points
        self.width = max(p[0] for p in points) + 1
        self.height = max(p[1] for p in points) + 1


WIDTH = 7
LINE = [(0, 0), (1, 0), (2, 0), (3, 0)]
PLUS = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
CORN = [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
PIPE = [(0, 0), (0, 1), (0, 2), (0, 3)]
CUBE = [(0, 0), (0, 1), (1, 0), (1, 1)]
ROCKS = [Shape(rock) for rock in [LINE, PLUS, CORN, PIPE, CUBE]]
ROCKS_LEN = len(ROCKS)


class Chamber:
    def __init__(self, jet_stream: list[int]) -> None:
        self.height = 0
        self.chamber = []
        self.shapes = cycle(ROCKS)
        self.rock_i = 0
        self.jets = cycle(jet_stream)
        self.jet_stream_len = len(jet_stream)
        self.jet_i = 0
        self.last_rock_top = 0

    def solve(self, count: int):
        """Each rock appears so that its left edge is two units away from the left wall and
        its bottom edge is three units above the highest rock in the room (or the floor,
        if there isn't one)"""

        # chamber starts as an empty grid of 7x4 (width x height)
        # reference position is the bottom-left corner
        # |0123456|  col
        # +-------+
        # |..####.|  row=0
        # |...#...|  row=1
        # |..###..|  row=2
        # |..R#...|  row=3  R=(x=2, y=3)
        # |.......|  row=4
        # |.......|  row=5
        for _ in range(count):
            falling, rock = True, self.next_rock()
            x, y = 2, 3 + self.height + rock.height
            self.expand(y)

            while falling:
                y -= 1
                # draw(chamber, rock, x, y, 2)  # where shape is before jet
                # draw(chamber, rock, x, y, 0)  # erase where shape is before jet
                x += apply_jet(self.chamber, rock, x, y, self.next_jet())
                falling = should_fall(self.chamber, rock, x, y)

                # draw(chamber, rock, x, y, 2)  # where shape is after jet
                # draw(chamber, rock, x, y, 0)  # erase where shape is after jet

            draw(self.chamber, rock, x, y, 1)  # where shape came to rest
            self.height = max(self.height, y + 1)

            # self.last_x = x
            # self.last_y = y
            # self.last_h = rock.height
            self.last_rock_top = y - rock.height

        return self.height

    def next_rock(self):
        self.rock_i = (self.rock_i + 1) % ROCKS_LEN
        return next(self.shapes)

    def next_jet(self):
        self.jet_i = (self.jet_i + 1) % self.jet_stream_len
        return next(self.jets)

    def expand(self, y: int):
        for _ in range(y - len(self.chamber)):
            self.chamber.append([0] * WIDTH)

    def has_blocking_row(self):
        """returns true if the last rock blocks the entire width such that
        future rocks cannot drop further"""
        full_row = set()
        for y in range(self.last_rock_top - 1, self.last_rock_top + 1):
            for x in range(WIDTH):
                if self.chamber[y][x] != 0:
                    full_row.add(x)
        return len(full_row) == WIDTH

    def state(self) -> str:
        """return a str representing the chamber's state for finding cycles in the simulation

        Each row of the chamber is a list of ones and zeros of length 7.
        Transform each row of the chamber into an int and sum them into a total
        """
        total = sum(transform_row_into_int(row) for row in self.chamber)

        return f'{total}|{self.rock_i}|{self.jet_i}'


def apply_jet(chamber, rock, x, y, jet_x: int) -> int:
    """returns jet_x rock can get jet in that direction, or 0 otherwise"""
    if jet_x < 0 and x == 0:
        return 0
    if jet_x > 0 and x + rock.width >= WIDTH:
        return 0
    for shape_x, shape_y in rock.points:
        row, col = y - shape_y, x + shape_x
        if chamber[row][col + jet_x] != 0:
            return 0
    return jet_x


def should_fall(chamber, rock, x, y) -> bool:
    for shape_x, shape_y in rock.points:
        row, col = y - shape_y, x + shape_x
        if row - 1 < 0 or chamber[row - 1][col] != 0:
            return False
    return True


def draw(chamber, rock, x, y, v):
    for shape_x, shape_y in rock.points:
        row, col = y - shape_y, x + shape_x
        chamber[row][col] = v  # draw where shape is


def sol2(jet_stream, count) -> int:
    chamber = Chamber(jet_stream)
    offset = 0
    states = {}  # previously seen chamber states
    num_blocks = 0

    while True:
        chamber.solve(1)  # simulate one rock falling
        num_blocks += 1

        if chamber.has_blocking_row():
            chamber.height -= chamber.last_rock_top
            chamber.chamber = chamber.chamber[chamber.last_rock_top:]
            offset += chamber.last_rock_top

        key = chamber.state()
        if key in states:
            prev_count, prev_height = states[key]
            cycle_len = num_blocks - prev_count
            if cycle_len < count - num_blocks:
                # We found a cycle...
                cycle_height = chamber.height + offset - prev_height
                ncycles = (count - num_blocks) // cycle_len
                num_blocks += ncycles * cycle_len
                offset += ncycles * cycle_height
        else:
            states[key] = (num_blocks, chamber.height + offset)

        if num_blocks == count:
            break

    return chamber.height + offset


def transform_row_into_int(rows: list[int]) -> int:
    return sum(j << i for i, j in enumerate(rows))


def test_sample():
    jet_stream = read('day17-sample.txt')
    chamber = Chamber(jet_stream)
    assert chamber.solve(count=2022) == 3068


def test_sample2():
    jet_stream = read('day17-sample.txt')
    assert sol2(jet_stream, count=1000000000000) == 1514285714288


def test_sol1():
    jet_stream = read('day17-input.txt')
    chamber = Chamber(jet_stream)
    assert chamber.solve(count=2022) == 3186


def test_sol2():
    jet_stream = read('day17-input.txt')
    assert sol2(jet_stream, count=1000000000000) == 1566376811584
