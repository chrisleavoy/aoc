def read(filename: str):
    data = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            data.append(line.strip())
    return data


OPEN = ['(', '[', '{', '<']
CLOSE = [')', ']', '}', '>']
POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}


def sol1(data):
    result = 0
    for line in data:
        stack = []
        for ch in line:
            if ch in OPEN:
                stack.append(ch)
            elif ch in CLOSE:
                if len(stack) == 0:
                    result += POINTS[ch]
                    break
                last = stack.pop()
                if OPEN.index(last) != CLOSE.index(ch):
                    result += POINTS[ch]
                    break
            else:
                raise ValueError('oops')
    return result


def sol2(data):
    incomplete = []
    for line in data:
        stack = []
        invalid = False
        for ch in line:
            if ch in OPEN:
                stack.append(ch)
            elif ch in CLOSE:
                if len(stack) == 0:
                    invalid = True
                    break
                last = stack.pop()
                if OPEN.index(last) != CLOSE.index(ch):
                    invalid = True
                    break
            else:
                raise ValueError('oops')
        if not invalid and len(stack) > 0:
            score = 0
            for ch in reversed(stack):
                score = score * 5 + OPEN.index(ch) + 1
            incomplete.append(score)
    incomplete.sort()
    return incomplete[int(len(incomplete)/2)]


def test_sol1():
    assert sol1(read('day10-sample.txt')) == 26397
    assert sol1(read('day10-input.txt')) == 343863


def test_sol2():
    assert sol2(read('day10-sample.txt')) == 288957
    assert sol2(read('day10-input.txt')) == 2924734236
