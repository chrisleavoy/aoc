def read(filename: str):
    caves = Caves()
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            x, y = line.strip().split('-')
            caves.add(x, y)
    return caves


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.paths = []

    def add(self, next_cave: str):
        """add a path from this cave to another"""
        self.paths.append(next_cave)


class Caves:
    def __init__(self, data=[]):
        # str -> Cave
        self.caves = {}
        self.add_all(data)

    def add_all(self, data):
        for link in data:
            self.add(*link)
        return self

    def add(self, x: str, y: str):
        cavex = self.caves.get(x) or Cave(x)
        cavey = self.caves.get(y) or Cave(y)
        cavex.add(y)
        cavey.add(x)
        self.caves[x] = cavex
        self.caves[y] = cavey
        return self

    def find_paths(self, pos='start', visited={}, max_small_visits=1):
        if pos == 'end':
            return [pos]

        new_paths = []
        cave = self.caves[pos]

        visited = visited.copy()
        visited[pos] = visited.get(pos, 0) + 1

        if visited[pos] == 2 and pos.islower():
            max_small_visits = 1

        for next_pos in sorted(cave.paths):
            if next_pos == 'start':
                continue  # going back to start isn't valid
            if next_pos.islower() and visited.get(next_pos, 0) >= max_small_visits:
                continue
            for path in self.find_paths(next_pos, visited, max_small_visits):
                new_paths.append(pos + ',' + path)
        return new_paths


def test_base():
    assert Caves().add('start', 'end').find_paths() == ['start,end']

    assert Caves(
        [('start', 'x'), ('x', 'end')]).find_paths() == ['start,x,end']

    assert Caves(
        [('start', 'x'), ('x', 'y'), ('y', 'end')]).find_paths() == ['start,x,y,end']

    assert Caves([('start', 'A'), ('start', 'b'),
                  ('A', 'b'), ('A', 'end'), ('b', 'end')]).find_paths() == [
        'start,A,b,A,end', 'start,A,b,end', 'start,A,end', 'start,b,A,end', 'start,b,end']


def test_paths():
    paths = [
        'start,A,b,A,c,A,end',
        'start,A,b,A,end',
        'start,A,b,end',
        'start,A,c,A,b,A,end',
        'start,A,c,A,b,end',
        'start,A,c,A,end',
        'start,A,end',
        'start,b,A,c,A,end',
        'start,b,A,end',
        'start,b,end'
    ]

    assert paths == sorted(paths)

    caves = read('day12-sample.txt')
    assert caves.find_paths() == paths


def test_sol1():
    assert len(read('day12-sample.txt').find_paths()) == 10
    assert len(read('day12-sample2.txt').find_paths()) == 19
    assert len(read('day12-sample3.txt').find_paths()) == 226
    assert len(read('day12-input.txt').find_paths()) == 5076


def test_base2():
    assert Caves().add('start', 'end').find_paths(
        max_small_visits=2) == ['start,end']

    assert Caves([('start', 'x'), ('x', 'end')]).find_paths(
        max_small_visits=2) == ['start,x,end']

    assert Caves([('start', 'x'), ('x', 'y'), ('y', 'end')]).find_paths(
        max_small_visits=2) == ['start,x,y,end']

    assert Caves([('start', 'A'), ('start', 'b'),
                  ('A', 'b'), ('A', 'end'), ('b', 'end')]).find_paths(
        max_small_visits=2) == [
            'start,A,b,A,b,A,end',
            'start,A,b,A,b,end',
            'start,A,b,A,end',
            'start,A,b,end',
            'start,A,end',
            'start,b,A,b,A,end',
            'start,b,A,b,end',
            'start,b,A,end',
            'start,b,end'
    ]


def test_paths2():
    assert read('day12-sample.txt').find_paths(max_small_visits=2) == [
        'start,A,b,A,b,A,c,A,end',
        'start,A,b,A,b,A,end',
        'start,A,b,A,b,end',
        'start,A,b,A,c,A,b,A,end',
        'start,A,b,A,c,A,b,end',
        'start,A,b,A,c,A,c,A,end',
        'start,A,b,A,c,A,end',
        'start,A,b,A,end',
        'start,A,b,d,b,A,c,A,end',
        'start,A,b,d,b,A,end',
        'start,A,b,d,b,end',
        'start,A,b,end',
        'start,A,c,A,b,A,b,A,end',
        'start,A,c,A,b,A,b,end',
        'start,A,c,A,b,A,c,A,end',
        'start,A,c,A,b,A,end',
        'start,A,c,A,b,d,b,A,end',
        'start,A,c,A,b,d,b,end',
        'start,A,c,A,b,end',
        'start,A,c,A,c,A,b,A,end',
        'start,A,c,A,c,A,b,end',
        'start,A,c,A,c,A,end',
        'start,A,c,A,end',
        'start,A,end',
        'start,b,A,b,A,c,A,end',
        'start,b,A,b,A,end',
        'start,b,A,b,end',
        'start,b,A,c,A,b,A,end',
        'start,b,A,c,A,b,end',
        'start,b,A,c,A,c,A,end',
        'start,b,A,c,A,end',
        'start,b,A,end',
        'start,b,d,b,A,c,A,end',
        'start,b,d,b,A,end',
        'start,b,d,b,end',
        'start,b,end'
    ]


def test_sol2():
    assert len(read('day12-sample.txt').find_paths(max_small_visits=2)) == 36
    assert len(read('day12-sample2.txt').find_paths(max_small_visits=2)) == 103
    assert len(read('day12-sample3.txt').find_paths(max_small_visits=2)) == 3509
    assert len(read('day12-input.txt').find_paths(max_small_visits=2)) == 145643
