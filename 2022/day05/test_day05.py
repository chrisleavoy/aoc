from pathlib import Path


def read(filename: str) -> list[str]:
    path = Path(__file__).parent.joinpath(filename)
    with open(path, encoding='utf-8') as f:
        return f.readlines()


def parse(lines: list[str]):
    n = (len(lines[0]) + 1) // 4
    stacks = [[] for _ in range(n)]
    for line in lines:
        if line == '\n':
            break
        for i in range(n):
            ch = line[1+i*4]
            if ch == '1' or ch == ' ':
                continue
            stacks[i].append(ch)

    moves = [
        (int(p[1]), int(p[3]), int(p[5])) for line in lines[10:] if (p := line.strip().split(' '))
    ]

    return stacks, moves


def test_sol1():
    s = read('day05-input.txt')
    stacks, moves = parse(s)
    for count, src, dst in moves:
        for _ in range(count):
            ch = stacks[src-1].pop(0)
            stacks[dst-1].insert(0, ch)

    top = ''.join([stack.pop(0) for stack in stacks])

    assert top == 'HBTMTBSDC'


def test_sol2():
    s = read('day05-input.txt')
    stacks, moves = parse(s)
    for count, src, dst in moves:
        moving = stacks[src-1][0:count]
        del stacks[src-1][:count]
        stacks[dst-1] = moving + stacks[dst-1]

    top = ''.join([stack.pop(0) for stack in stacks])

    assert top == 'PQTJRSHWS'
