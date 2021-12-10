def read(filename: str):
    data = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            data.append(line.strip())
    return data


def sol1(data):
    result = 0
    return result


def sol2(data):
    result = 0
    return result


def test_sol1():
    assert sol1(read('day0-sample.txt')) == 0
    assert sol1(read('day0-input.txt')) == 0


def test_sol2():
    assert sol2(read('day0-sample.txt')) == 0
    assert sol2(read('day0-input.txt')) == 0
