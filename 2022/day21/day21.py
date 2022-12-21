import unittest
from dataclasses import dataclass
from pathlib import Path

from sympy import solve

ROOT, HUMAN = 'root', 'humn'


Formula = str | tuple[str, str, str]
Input = dict[str, Formula]


def puzzle_input(filename: str = 'day21-input.txt') -> Input:
    with open(Path(__file__).parent.joinpath(filename), encoding='utf-8') as f:
        monkeys = {}
        for line in f.read().splitlines():
            monkey, formula = line[:4], line[6:]
            if not formula.isnumeric():
                formula = tuple(formula.split(' '))
            monkeys[monkey] = formula
        return monkeys


@dataclass
class Puzzle():
    monkeys: Input

    def expression(self, name=ROOT):
        formula = self.monkeys[name]
        if not isinstance(formula, tuple):
            return formula

        a = self.expression(formula[0])
        b = self.expression(formula[2])
        operator = formula[1]
        return f'({a} {operator} {b})'

    def solve1(self):
        exp = self.expression()
        # pylint: disable=eval-used
        return int(eval(exp))

    def solve2(self):
        root = self.monkeys[ROOT]
        self.monkeys[ROOT] = (root[0], '-', root[2])
        self.monkeys[HUMAN] = 'humn'
        exp = self.expression()  # solve for humn where exp == 0
        return solve(exp)[0]


if __name__ == '__main__':
    sample = Puzzle(puzzle_input('day21-sample.txt'))
    sample1 = sample.solve1()
    print(f'{sample1=}')
    sample2 = sample.solve2()
    print(f'{sample2=}')

    puzzle = Puzzle(puzzle_input())
    puzzle1 = puzzle.solve1()
    print(f'{puzzle1=}')
    puzzle2 = puzzle.solve2()
    print(f'{puzzle2=}')

    tc = unittest.TestCase()
    tc.assertEqual(sample1, 152)
    tc.assertEqual(sample2, 301)
    tc.assertEqual(puzzle1, 379578518396784)
    tc.assertEqual(puzzle2, 3353687996514)
