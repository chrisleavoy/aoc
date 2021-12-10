def read(filename: str):
    data = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            data.append([int(x) for x in line.strip()])
    return data


def low_points(data):
    lows = []
    rows = len(data)
    cols = len(data[0])
    for row in range(rows):
        for col in range(cols):
            lh = col > 0 and data[row][col-1] <= data[row][col]
            th = row > 0 and data[row-1][col] <= data[row][col]
            rh = col < cols - 1 and data[row][col+1] <= data[row][col]
            bh = row < rows - 1 and data[row+1][col] <= data[row][col]
            if lh or rh or th or bh:
                continue
            lows.append((row, col))
    return lows


def sol1(data):
    result = 0
    for row, col in low_points(data):
        result += 1 + data[row][col]
    return result


def sol2(data):
    basins = []
    for low in low_points(data):
        basin_size = calc(*low, data)
        basins.append(basin_size)
    top = sorted(basins, reverse=True)[0:3]
    return top[0] * top[1] * top[2]


def calc(row, col, data):
    if row < 0 or col < 0:
        return 0
    if row > len(data) - 1 or col > len(data[0]) - 1:
        return 0
    if data[row][col] == 9:
        return 0
    data[row][col] = 9
    lr = calc(row-1, col, data) + calc(row+1, col, data)
    ud = calc(row, col-1, data) + calc(row, col+1, data)
    return 1 + lr + ud


def test_sol1():
    assert sol1(read('day9-sample.txt')) == 15
    assert sol1(read('day9-input.txt')) == 528


def test_sol2():
    assert sol2(read('day9-sample.txt')) == 1134
    assert sol2(read('day9-input.txt')) == 920448
