from pathlib import Path

ROCK1, PAPE1, SCIS1 = "A", "B", "C"
ROCK2, PAPE2, SCIS2 = "X", "Y", "Z"
SCORES = {ROCK2: 1, PAPE2: 2, SCIS2: 3}
LOSE, DRAW, WIN = "X", "Y", "Z"
SOLVER = {
    WIN: {ROCK1: PAPE2, SCIS1: ROCK2, PAPE1: SCIS2},
    DRAW: {ROCK1: ROCK2, SCIS1: SCIS2, PAPE1: PAPE2},
    LOSE: {ROCK1: SCIS2, SCIS1: PAPE2, PAPE1: ROCK2},
}


def read(filename: str) -> list[str]:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return f.read().splitlines()


def outcome(p1, p2):
    """returns 1 when player 2 (us) wins, 0 on draw and -1 on a loss"""
    if p2 == ROCK2 and p1 == SCIS1 or p2 == PAPE2 and p1 == ROCK1 or p2 == SCIS2 and p1 == PAPE1:
        return score(1, p2,)
    if p2 == ROCK2 and p1 == ROCK1 or p2 == PAPE2 and p1 == PAPE1 or p2 == SCIS2 and p1 == SCIS1:
        return score(0, p2)
    return score(-1, p2)


def outcome2(p1, result):
    p2 = SOLVER[result][p1]
    return outcome(p1, p2)


def score(result: int, p2: str):
    return result, SCORES[p2] + 3 * (result + 1)


def test_winner():
    assert outcome(ROCK1, PAPE2) == (1, 8)
    assert outcome(ROCK1, SCIS2) == (-1, 3)
    assert outcome(ROCK1, ROCK2) == (0, 4)


def test_sample():
    assert outcome('A', 'Y') == (1, 8)
    assert outcome('B', 'X') == (-1, 1)
    assert outcome('C', 'Z') == (0, 6)


def test_sample2():
    assert outcome2('A', 'Y') == (0, 4)
    assert outcome2('B', 'X') == (-1, 1)
    assert outcome2('C', 'Z') == (1, 7)


def test_sol1():
    lines = read('day02-input.txt')
    total = 0
    for line in lines:
        p1, p2 = line.split(' ')
        _, s = outcome(p1, p2)
        total += s
    assert total == 11841


def test_sol2():
    lines = read('day02-input.txt')
    total = 0
    for line in lines:
        p1, result = line.split(' ')
        _, s = outcome2(p1, result)
        total += s
    assert total == 13022
