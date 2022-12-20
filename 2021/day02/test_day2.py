from pathlib import Path


def read(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        lines = [line.strip().split() for line in f]
        return lines


def movement(inputs):
    x = 0
    d = 0
    for line in inputs:
        v = int(line[1])
        if line[0] == 'forward':
            x += v
        elif line[0] == 'down':
            d += v
        elif line[0] == 'up':
            d -= v
        else:
            raise ValueError(f'line "{line}" is not valid')
    return (x, d, x*d)


def movement2(inputs):
    x = 0
    d = 0
    aim = 0
    for line in inputs:
        v = int(line[1])
        if line[0] == 'forward':
            x += v
            d += aim * v
        elif line[0] == 'down':
            aim += v
        elif line[0] == 'up':
            aim -= v
        else:
            raise ValueError(f'line "{line}" is not valid')
    return (x, d, x*d)


def test_1():
    assert movement(read('day2-sample.txt')) == (15, 10, 150)
    assert movement(read('day2-input.txt')) == (2003, 980, 1962940)


def test_2():
    assert movement2(read('day2-sample.txt')) == (15, 60, 900)
    assert movement2(read('day2-input.txt')
                     ) == (2003, 905474, 1813664422)

# print(read('day2-sample.txt'))
# print(read('day2-input.txt'))
