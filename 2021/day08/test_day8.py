from pathlib import Path


def read(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    data = []
    with open(path, encoding='utf-8') as f:
        for line in f.readlines():
            signals, output = line.strip().split(' | ')
            data.append((signals, output))
    return data


def sol1(data):
    count = 0
    unique = [2, 4, 3, 7]
    for entry in data:
        _, output = entry
        for display in output.split():
            if len(display) in unique:
                count += 1
    return count


def decode(signals, output):
    # pattern (sorted) -> digit
    result = {}

    # digit -> pattern
    lookup = {}

    # segment count -> digit
    unique = {
        2: 1,
        4: 4,
        3: 7,
        7: 8
    }

    fives = []
    sixes = []
    for display in signals.split() + output.split():
        segments = len(display)
        k = sort_key(display)
        digit = unique.get(segments)
        if digit is not None:
            result[k] = digit
            lookup[digit] = k
        elif segments == 5:
            fives.append(k)
        elif segments == 6:
            sixes.append(k)
        else:
            raise ValueError('impossible segment count')

    for ch in lookup.get(7):
        # 7 is a subset 0 and 9 but not 6
        for p in sixes:
            if ch not in p:
                result[p] = 6
                lookup[6] = p
                sixes.remove(p)
                break
        if lookup.get(6) is not None:
            break

    # know: c - its the segment of 7 missing from 6
    for c in lookup.get(7):
        if c not in lookup.get(6):
            for p in fives:
                if c not in p:
                    # know: 5 is missing c
                    result[p] = 5
                    lookup[5] = p
                    fives.remove(p)
                    break
            break

    # we know 1, 4, 7, 8 have unique counts
    # we know 2, 3, 5 have 5 segments
    # we know 0, 6, 9 have 6 segments
    # we know 6, as 7 is a subset 0 and 9 but not 6
    # we know c, as it the segment of 7 missing from 6
    # we know 5, as its missing segment c
    # unknowns:
    # 5s - 2,3
    # 6s - 0,9
    # we know 0 & 9, as 4 is a subset of 9 but not 0
    for ch in lookup.get(4):
        # ch=d is not in 0, but is in 9
        if ch not in sixes[0]:
            lookup[0] = sixes[0]
            lookup[9] = sixes[1]
            break
        elif ch not in sixes[1]:
            lookup[0] = sixes[1]
            lookup[9] = sixes[0]
            break
    result[lookup[0]] = 0
    result[lookup[9]] = 9

    # we know 2 & 3, as 1 is a subset of 3 but not 2
    for ch in lookup.get(1):
        # ch=f is not in 2, but is in 3
        if ch not in fives[0]:
            lookup[2] = fives[0]
            lookup[3] = fives[1]
            break
        elif ch not in fives[1]:
            lookup[2] = fives[1]
            lookup[3] = fives[0]
            break
    result[lookup[2]] = 2
    result[lookup[3]] = 3

    return result


def sort_key(k):
    return ''.join(sorted(k))


def encode(digits, output):
    num = 0
    for display in output.split():
        digit = digits.get(sort_key(display))
        if digit is None:
            raise ValueError('oops')
        num = num * 10 + digit
    return num


def sol2(data):
    result = 0
    for entry in data:
        signals, output = entry
        digits = decode(signals, output)
        result += encode(digits, output)
    return result


def solve(entry):
    signals, output = entry
    return encode(decode(signals, output), output)


def test_sol1():
    assert sol1(read('day8-sample.txt')) == 26
    assert sol1(read('day8-input.txt')) == 349


def test_sol2():
    signals = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab'
    output = 'cdfeb fcadb cdfeb cdbaf'
    assert solve((signals, output)) == 5353

    data = read('day8-sample.txt')
    assert solve(data[0]) == 8394

    assert sol2(read('day8-sample.txt')) == 61229
    assert sol2(read('day8-input.txt')) == 1070957
