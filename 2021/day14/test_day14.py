from pathlib import Path


def read(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    rules = {}
    with open(path, encoding='utf-8') as f:
        template = f.readline().strip()
        f.readline()
        for line in f.readlines():
            x, _, y = line.strip().split()
            rules[x] = y
    return (template, rules)


def get_polymer(template, rules, steps):
    polymer = template
    for _ in range(steps):
        p = template[0]
        for i in range(len(polymer)-1):
            pair = polymer[i:i+2]
            rule = rules[pair]
            p = p + rule + pair[-1]
        polymer = p
    return polymer


def test_get_polymer():
    template, rules = read('day14-sample.txt')
    assert get_polymer('NC', rules, 1) == 'NBC'
    assert get_polymer('NC', rules, 2) == 'NBBBC'
    assert get_polymer('NC', rules, 3) == 'NBBNBNBBC'
    assert get_polymer(template, rules, 1) == 'NCNBCHB'
    assert get_polymer(template, rules, 2) == 'NBCCNBBBCBHCB'
    assert get_polymer(template, rules, 3) == 'NBBBCNCCNBBNBNBBCHBHHBCHB'
    assert get_polymer(template, rules, 4
                       ) == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    assert len(get_polymer(template, rules, 5)) == 97
    polymer = get_polymer(template, rules, 10)
    assert len(polymer) == 3073


def calc(polymer):
    d = {}
    mce = (None, -1)
    for ch in polymer:
        d[ch] = d.get(ch, 0) + 1
        if d[ch] > mce[1]:
            mce = (ch, d[ch])
    lce = mce
    for ch, count in d.items():
        if count < lce[1]:
            lce = (ch, count)
    return mce[1] - lce[1]


def sol1(template, rules, steps=10):
    polymer = get_polymer(template, rules, steps)
    return calc(polymer)


def test_sol1():
    assert sol1(*read('day14-sample.txt')) == 1588
    assert sol1(*read('day14-input.txt')) == 2891


#
# after we've used brute force, we try something more elegant
#


def get_pairs(template, rules, steps=10):
    # each starting pair produces a left and right pair
    # NC    -> NBC         -> 2>3   -> NB, BC
    # NBC   -> NBBBC       -> 3>5   -> NB->NBB(NB,BC), BC-> BBC(BB,BC)
    # NBBBC -> NBBNBNBBC   -> 5->9
    #
    # get a map of pairs -> count:
    pairs = pair_count(template)

    for _ in range(steps):
        results = {}
        for pair, count in pairs.items():
            ch = rules[pair]
            lp = pair[0] + ch
            rp = ch + pair[-1]
            results[lp] = results.get(lp, 0) + count
            results[rp] = results.get(rp, 0) + count
        pairs = results
    return pairs


def sol2(template, rules, steps=10):
    pairs = get_pairs(template, rules, steps)
    counts = get_counts(pairs)
    counts[template[-1]] += 1
    result = max(counts.values()) - min(counts.values())
    return result


def get_counts(pairs):
    counts = {}
    for pair, count in pairs.items():
        counts[pair[0]] = counts.get(pair[0], 0) + count
    return counts


def split_pairs(polymer):
    pairs = []
    for i in range(len(polymer)-1):
        pairs.append(polymer[i:i+2])
    return pairs


def pair_count(polymer):
    pairs = {}
    for pair in split_pairs(polymer):
        pairs[pair] = pairs.get(pair, 0) + 1
    return pairs


def test_get_pairs():
    template, rules = read('day14-sample.txt')  # 'NNCB'

    assert get_pairs(template, rules, 1) == pair_count('NCNBCHB')
    assert get_pairs(template, rules, 2) == pair_count('NBCCNBBBCBHCB')
    assert get_pairs(template, rules, 3) == pair_count(
        'NBBBCNCCNBBNBNBBCHBHHBCHB')
    assert get_pairs(template, rules, 4) == pair_count(
        'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')

    assert sum(get_pairs(template, rules, 5).values()) + 1 == 97
    assert sum(get_pairs(template, rules, 10).values()) + 1 == 3073


def test_sol2():
    template, rules = read('day14-sample.txt')
    polymer = get_polymer(template, rules, 10)
    assert len(polymer) == 3073
    pc = pair_count(polymer)

    _, rules = read('day14-sample.txt')
    stepX = get_pairs(template, rules, 10)
    assert stepX == pc

    assert sol2(*read('day14-sample.txt'), 10) == 1588
    assert sol2(*read('day14-input.txt'), 10) == 2891

    assert sol2(*read('day14-sample.txt'), 40) == 2188189693529
    assert sol2(*read('day14-input.txt'), 40) == 4607749009683


def test_helpers():
    assert split_pairs('NC') == ['NC']
    assert split_pairs('NBC') == ['NB', 'BC']
    assert split_pairs('NBCD') == ['NB', 'BC', 'CD']

    assert pair_count('NC') == {'NC': 1}
    assert pair_count('NBC') == {'NB': 1, 'BC': 1}
    assert pair_count('NBCD') == {'NB': 1, 'BC': 1, 'CD': 1}
