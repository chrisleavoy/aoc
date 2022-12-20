from pathlib import Path


def read(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        calories, elves = 0, []
        for line in f.readlines():
            l = line.strip()
            if l == "":
                elves.append(calories)
                calories = 0
            else:
                calories += int(l)
        elves.append(calories)
        return elves


def test_sol1():
    elves = read('day01-input.txt')
    assert max(elves) == 69795


def test_sol2():
    elves = read('day01-input.txt')
    elves.sort()
    sum_top3 = sum(elves[-3:])
    assert sum_top3 == 208437
