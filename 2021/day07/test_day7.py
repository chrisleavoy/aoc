from pathlib import Path


def read(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return [int(x) for x in f.read().strip().split(',')]


def sol1(data):
    leastFuel = -1
    for i in range(min(data), max(data)):
        fuel = 0
        for x in data:
            fuel += abs(x - i)
        if leastFuel == -1 or fuel < leastFuel:
            leastFuel = fuel
    return leastFuel


def sol2(data):
    leastFuel = -1
    mean = int(sum(data) / len(data))
    for x in range(mean-1, mean+2):
        fuel = 0
        for y in data:
            fuel += cost(x, y)
        if leastFuel == -1 or fuel < leastFuel:
            leastFuel = fuel
    return leastFuel


def cost(x, y):
    n = abs(x-y)
    return int(n*(n+1)/2)


def test_1():
    assert sol1([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]) == 37
    assert sol1(read('day7-input.txt')) == 329389


def test_2():
    assert cost(2, 5) == 6
    assert cost(0, 5) == 15
    assert cost(1, 5) == 10
    assert cost(16, 5) == 66
    assert cost(4, 5) == 1
    assert cost(2, 5) == 6
    assert cost(7, 5) == 3
    assert cost(14, 5) == 45

    assert sol2([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]) == 168
    assert sol2(read('day7-input.txt')) == 86397080
