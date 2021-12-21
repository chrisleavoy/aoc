from pathlib import Path


def read(filename: str):
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        lines = [line.strip() for line in f]
        return lines


def fn1(inputs):
    n = len(inputs)
    m = len(inputs[0])
    counts = [0] * m
    for line in inputs:
        for i, ch in enumerate(line):
            if ch == '1':
                counts[i] += 1

    gamma = ''
    for count in counts:
        if count > n/2:
            gamma += '1'
        else:
            gamma += '0'

    epsilon = ''.join(['0' if i == '1' else '1' for i in gamma])

    return int(gamma, 2) * int(epsilon, 2)


def fn2(inputs):
    n = len(inputs)
    m = len(inputs[0])
    remainders = range(n)
    ogr = ''
    co2 = ''

    for i in range(m):  # for each bit position
        ones = []
        zeros = []
        for r in remainders:
            if inputs[r][i] == '1':
                ones.append(r)
            else:
                zeros.append(r)
        if len(ones) >= len(zeros):
            remainders = ones
        else:
            remainders = zeros
        if len(remainders) == 1:
            ogr = inputs[remainders[0]]
            break

    remainders = range(n)
    for i in range(m):  # for each bit position
        ones = []
        zeros = []
        for r in remainders:
            if inputs[r][i] == '1':
                ones.append(r)
            else:
                zeros.append(r)
        if len(ones) < len(zeros):
            remainders = ones
        else:
            remainders = zeros
        if len(remainders) == 1:
            co2 = inputs[remainders[0]]
            break

    return int(ogr, 2) * int(co2, 2)


def test_1():
    assert fn1(read('day3-sample.txt')) == 198
    assert fn1(read('day3-input.txt')) == 2003336


def test_2():
    assert fn2(read('day3-sample.txt')) == 230
    assert fn2(read('day3-input.txt')) == 1877139

# print(inputs('day3-sample.txt'))
# print(inputs('day2-input.txt'))
