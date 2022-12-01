from pathlib import Path


def sol1(state, days):
    for _ in range(days):
        births = 0
        for i in range(len(state)):
            if state[i] == 0:
                state[i] = 6
                births += 1
            else:
                state[i] -= 1
        state = state + [8]*births
    return len(state)


def sol2(state, days):
    STATES = 9
    counts = [0]*STATES
    for c in state:
        counts[c] += 1
    for _ in range(days):
        births = counts[0]
        for i in range(STATES - 1):
            counts[i] = counts[i+1]
        # 8s -> 7s
        # 7s -> 6s
        # ...
        # 1s -> 0s
        # 0s -> 6s + 8s
        counts[6] += births
        counts[8] = births

    return sum(counts)


def read(filename: str):
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return [int(x) for x in f.read().strip().split(',')]


def sample_input():
    return [3, 4, 3, 1, 2]


def test_sol1():
    assert sol1(sample_input(), days=1) == 5
    assert sol1(sample_input(), days=2) == 6
    assert sol1(sample_input(), days=18) == 26
    assert sol1(sample_input(), days=80) == 5934

    state = read('day6-input.txt')
    assert sol1(state, days=80) == 362639


def test_sol2():
    assert sol2(sample_input(), days=2) == 6
    assert sol2(sample_input(), days=18) == 26
    assert sol2(sample_input(), days=80) == 5934
    assert sol2(sample_input(), days=256) == 26984457539

    state = read('day6-input.txt')
    assert sol2(state, days=256) == 1639854996917
