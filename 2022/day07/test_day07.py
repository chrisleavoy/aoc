from pathlib import Path
from typing import Self, Optional


class Node():
    def __init__(self, name='/', kind='d', size=0, parent: Optional[Self] = None) -> None:
        self.name = name
        self.kind = kind
        self.size = size
        self.parent = parent
        self.children: dict[str, Node] = {}

    def __repr__(self):
        return self.name

    def add(self, c):
        if isinstance(c, Node):
            c.parent = self
            if c.name not in self.children:
                self.children[c.name] = c

    def total_size(self):
        total = self.size + sum([
            c.total_size() for _, c in self.children.items()
        ])
        return total

    def filtered_size(self):
        total = self.total_size()
        local = total if total <= 100000 and self.kind == 'd' else 0
        nested = sum([
            c.filtered_size() for _, c in self.children.items()
        ])
        return local + nested

    def find_smallest_of(self, atleast: int):
        smallest = self.total_size()

        for _, c in self.children.items():
            if c.kind == 'd':
                total = c.total_size()
                if total >= atleast:
                    smallest = min(smallest, c.find_smallest_of(atleast))

        return smallest


def read(filename: str) -> list[str]:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return f.read().splitlines(keepends=False)


def parse(filename: str) -> Node:
    lines = read(filename)
    root = Node('/')
    current = root

    for cmd in lines:
        if cmd == "$ cd /":
            current = root
        elif cmd.startswith('$ cd ..'):
            current = current.parent
        elif cmd.startswith('$ cd'):
            name = cmd[5:]
            c = current.children.get(name)
            current = c
        elif cmd == '$ ls':
            continue
        elif cmd.startswith('dir '):
            name = cmd[4:]
            d = Node(name)
            current.add(d)
        else:
            size, name = cmd.split(' ', maxsplit=2)
            f = Node(name, kind='f', size=int(size))
            current.add(f)
    return root


capacity = 70000000
needed = 30000000


def test_sample1():
    root = parse('day07-sample.txt')
    used = root.total_size()
    assert root.filtered_size() == 95437
    assert used == 48381165
    required = needed - (capacity - used)
    assert required == 8381165
    assert root.find_smallest_of(required) == 24933642


def test_sol1():
    root = parse('day07-input.txt')
    used = root.total_size()
    assert root.filtered_size() == 1845346
    required = needed - (capacity - used)
    # find smallest dir with at least the required total size
    assert root.find_smallest_of(required) == 3636703
