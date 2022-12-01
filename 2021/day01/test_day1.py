from pathlib import Path


def measurements(filename: str):
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf8') as f:
        return [line.strip() for line in f]


def measurements2(filename: str):
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf8') as f:
        return [int(line.strip()) for line in f]


def solution1(filename: str):
    m = measurements(filename)
    c = 0
    prev = m[0]
    for last in m[1:]:
        if last > prev:
            c += 1

        # string!!!
        if int(last) > int(prev) and not last > prev:
            print(f'wtf {last} {prev}')

        prev = last
    return c


def solution2(filename: str):
    m = measurements2(filename)
    c = 0
    wz = 3

    for i in range(len(m) - wz + 1):
        w1 = sum(m[i:i+wz])
        w2 = sum(m[i+1:i+1+wz])
        if w2 > w1:
            c += 1

    return c


def test_1():
    assert solution1('day1-sample.txt') == 7
    assert solution1('day1-input.txt') == 1445


def test_2():
    assert solution2('day1-sample.txt') == 5
    assert solution2('day1-input.txt') == 1486
