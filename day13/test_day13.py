from pathlib import Path


def read(filename: str):
    filename = Path(__file__).parent / filename
    data = []
    maxX = -1
    maxY = -1
    with open(filename, encoding='utf-8') as f:
        folds = None
        for line in f.readlines():
            line = line.strip()
            if line == '':
                folds = []
            elif folds is not None:
                _, _, fold = line.split()
                folds.append(fold)
            else:
                x, y = line.split(',')
                x = int(x)
                y = int(y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)
                data.append((x, y))
        grid = []*(maxY+1)
        for y in range(maxY+1):
            grid.append(['.']*(maxX+1))
        for x, y in data:
            grid[y][x] = '#'
    return (grid, folds)


def sol1(data, break_early=True):
    grid, folds = data
    for f in folds:
        axis, num = f.split('=')
        num = int(num)
        grid = fold(grid, axis, num)
        if break_early:
            break
    result = 0
    for row in grid:
        for col in row:
            result += 1 if col == '#' else 0
    return result


def fold(grid, axis, num):
    if axis == 'y':
        # assert len(grid)/2 == num
        for y in range(num):
            for x in range(len(grid[y])):
                mirror = len(grid) - y - 1
                if grid[mirror][x] == '#':
                    grid[y][x] = '#'
            # grid[y] = grid[y][:num]
        return grid[:num]
    if axis == 'x':
        length = len(grid[0])
        assert length/2 == num
        for y in range(len(grid)):
            for x in range(num):
                mirror = len(grid[y]) - x - 1
                if grid[y][mirror] == '#':
                    grid[y][x] = '#'
            grid[y] = grid[y][:num]
        return grid
    raise ValueError('oops')


def test_fold():
    assert fold([['.', '.']], 'x', 1) == [['.']]
    assert fold([['.', '#']], 'x', 1) == [['#']]
    assert fold([['#', '.']], 'x', 1) == [['#']]
    assert fold([['#', '#']], 'x', 1) == [['#']]
    # odd folds?
    # folds outside middle?
    # assert fold([['.', '.', '#']], 'x', 2) == [['.', '#']]

    assert fold([['.', '#'], ['.', '#']], 'x', 1) == [['#'], ['#']]
    assert fold([['.', '.', '#', '.', '#', '#']], 'x', 3) == [['#', '#', '#']]
    assert fold([['.', '.', '.', '#', '#', '#']], 'x', 3) == [['#', '#', '#']]
    assert fold([['#', '#', '#', '.', '.', '.']], 'x', 3) == [['#', '#', '#']]
    assert fold([['.', '.', '.', '.', '.', '.']], 'x', 3) == [['.', '.', '.']]


def sol2(data):
    result = 0
    return result


# def test_read():
#     assert read('day13-sample.txt') == ([], [])


def test_sol1():
    assert sol1(read('day13-sample.txt')) == 17
    assert sol1(read('day13-input.txt')) == 602


def test_sol2():
    assert sol2(read('day13-input.txt')) == 0
