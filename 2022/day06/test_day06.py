from pathlib import Path


def read(filename: str) -> str:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return f.read().strip()


def sol(s: str, distinct: int = 4) -> int:
    for i in range(distinct, len(s)):
        if len(set(s[i-distinct:i])) == distinct:
            return i
    return -1


def test_sol1():
    assert sol('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
    assert sol('nppdvjthqldpwncqszvftbrmjlhg') == 6
    assert sol('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
    assert sol('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11
    s = read('day06-input.txt')
    assert sol(s) == 1896


def test_sol2():
    assert sol('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert sol('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert sol('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert sol('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert sol('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26
    s = read('day06-input.txt')
    assert sol(s, 14) == 3452
