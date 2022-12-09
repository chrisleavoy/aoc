from pathlib import Path


def read(filename: str) -> list[str]:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return f.read().splitlines(keepends=False)


def sol(lines, segments=2) -> int:
    # x/y coordinate positions of rope segments:
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(segments)]
    # x/y coordinate positions of where the tail visits:
    visited: dict[tuple[int, int], bool] = {(0, 0): True}

    for line in lines:
        d, v = line.split(' ')
        v = int(v)
        vx = 1 if d == 'U' else (-1 if d == 'D' else 0)
        vy = 1 if d == 'R' else (-1 if d == 'L' else 0)

        for _ in range(0, v):  # for each step
            for segment in range(segments):
                if segment == 0:  # head moves first
                    hx, hy = rope[segment]
                    hx += vx
                    hy += vy
                    rope[segment] = (hx, hy)
                else:  # then each segment moves
                    hx, hy = rope[segment-1]
                    tx, ty = rope[segment]
                    dx = hx - tx
                    dy = hy - ty

                    if abs(dx) > 2 or abs(dy) > 2:
                        raise ValueError('wtf')

                    if abs(dx) <= 1 and abs(dy) <= 1:  # touching
                        continue  # rope has slack, tail does not move

                    if abs(dx) >= 1 and abs(dy) >= 1:  # move diag
                        tx += 1 if dx > 0 else -1
                        ty += 1 if dy > 0 else -1
                    elif dx == 0 and dy == 2:  # same row, move r
                        ty += 1
                    elif dx == 0 and dy == -2:  # same row, move l
                        ty -= 1
                    elif dy == 0 and dx == 2:  # same col, move u
                        tx += 1
                    elif dy == 0 and dx == -2:  # same col, move d
                        tx -= 1
                    else:
                        raise ValueError('missing case')

                    if segment == segments - 1:  # track where the tail visits
                        visited[(tx, ty)] = True
                    rope[segment] = (tx, ty)

    return len(visited)


def test_sample():
    lines = read('day09-sample.txt')
    assert sol(lines) == 13


def test_sol1():
    lines = read('day09-input.txt')
    assert sol(lines) == 6503


def test_sol2():
    lines = read('day09-input.txt')
    assert sol(lines, 10) == 2724
