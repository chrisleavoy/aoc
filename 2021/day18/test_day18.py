from itertools import permutations
from typing import Type
from pathlib import Path


def read(filename: str):
    path = Path(__file__).parent.joinpath(filename)
    numbers = []
    with open(path, encoding='utf-8') as f:
        for line in f.readlines():
            # don't judge me pylint, this is a speed competition!
            # pylint: disable=eval-used
            num = eval(line.strip())
            numbers.append(num)
        return numbers


class Pair:
    def __init__(self, left=None, right=None, depth=0, parent=None):
        self.left = Pair(left[0], left[1], depth + 1,
                         self) if isinstance(left, list) else left
        self.right = Pair(right[0], right[1], depth + 1,
                          self) if isinstance(right, list) else right
        self.depth = depth
        self.parent = parent

    def isleaf(self):
        return isinstance(self.left, int) and isinstance(self.right, int)

    def pair(self):
        return (self.left, self.right)

    def arr(self):
        x = self.left if isinstance(self.left, int) else self.left.arr()
        y = self.right if isinstance(self.right, int) else self.right.arr()
        return [x, y]

    def magnitude(self):
        mag = 3 * \
            self.left if isinstance(
                self.left, int) else 3 * self.left.magnitude()
        mag += 2 * \
            self.right if isinstance(
                self.right, int) else 2 * self.right.magnitude()
        return mag


class SFNum:
    def __init__(self, a):
        left, right = a
        head_depth = 0
        head_parent = None
        self.pair = Pair(left, right, head_depth, head_parent)

    def find(self, either=False):
        """find the left most pair with depth 4
        also keep track of the first over pair and return over if either is True"""
        stack = [self.pair]
        while len(stack) > 0:
            curr = stack.pop()
            if curr.depth == 4:
                assert curr.isleaf()
                return curr
            if isinstance(curr.right, Pair):
                stack.append(curr.right)
            if isinstance(curr.left, Pair):
                stack.append(curr.left)
        if either:
            return self.find_over(self.pair)
        return None

    def find_over(self, curr: Type[Pair]):
        if isinstance(curr.left, int):
            if curr.left >= 10:
                return curr
        else:
            # if left is pair, search curr.left
            found = self.find_over(curr.left)
            if found is not None:
                return found
        if isinstance(curr.right, int):
            # then check right
            if curr.right >= 10:
                return curr
        else:
            # then if right is pair, search right
            found = self.find_over(curr.right)
            if found is not None:
                return found
        return None

    def split(self):
        pair = self.find(True)
        return self.split_pair(pair)

    def split_pair(self, pair):
        """To split a regular number, replace it with a pair; the left element
        of the pair should be the regular number divided by two and rounded
        down, while the right element of the pair should be the regular number
        divided by two and rounded up. For example, 10 becomes [5,5], 11
        becomes [5,6], 12 becomes [6,6], and so on"""
        if isinstance(pair.left, int) and pair.left >= 10:
            v = pair.left
            x = v // 2
            y = (v % 2 > 0) + x
            pair.left = Pair(x, y, pair.depth + 1, pair)
        elif isinstance(pair.right, int) and pair.right >= 10:
            v = pair.right
            x = v // 2
            y = (v % 2 > 0) + x
            pair.right = Pair(x, y, pair.depth + 1, pair)
        else:
            raise ValueError('oops')
        return self

    def reduce(self):
        # print('\n')
        print(self.arr(), "starting")
        pair = self.find(True)
        while pair is not None:
            # a = pair.arr()
            if pair.depth == 4:
                self.explode_pair(pair)
                print(self.arr())  # , f'  \texploded pair={a}')
            else:
                self.split_pair(pair)
                print(self.arr())  # , f'   \tsplit pair={a}')
            pair = self.find(True)
        print('reduced')
        return self

    def add(self, y):
        x = self.arr()
        self.pair = SFNum([x, y]).pair
        self.reduce()
        return self

    def arr(self):
        return self.pair.arr()

    def explode(self):
        pair = self.find()
        return self.explode_pair(pair)

    def explode_pair(self, pair):
        if pair is not None:
            x, y = pair.left, pair.right  # given (x, y) in leaf pair=pair
            # add x to left most number (if any)
            add_left(pair.parent, x, pair)
            # add y to right most number (if any)
            add_right(pair.parent, y, pair)
            # replace exploding pair with a zero
            if pair == pair.parent.left:
                pair.parent.left = 0
            elif pair == pair.parent.right:
                pair.parent.right = 0
            return self
        return None

    def magnitude(self):
        return self.pair.magnitude()


def add_left(curr: Type[Pair], v: int, prev: Type[Pair]):
    """ add v to the left of curr (if any)"""
    while True:
        if isinstance(curr.left, int):
            curr.left += v
            return
        if prev == curr.right:
            # traverse the right side of curr.left to the right most node
            curr = traverse_right(curr.left)
            curr.right += v
            return
        if curr.parent is None:
            return
        prev = curr
        curr = curr.parent


def add_right(curr: Type[Pair], v: int, prev: Type[Pair]):
    """ add v to the right of curr if any)"""
    while True:
        if isinstance(curr.right, int):
            curr.right += v
            return
        if prev == curr.left:
            # traverse the left side of curr.right to the left most node
            curr = traverse_left(curr.right)
            curr.left += v
            return
        if curr.parent is None:
            return
        prev = curr
        curr = curr.parent


def traverse_left(curr: Type[Pair]):
    while True:
        if isinstance(curr.left, int):
            return curr
        curr = curr.left


def traverse_right(curr: Type[Pair]):
    while True:
        if isinstance(curr.right, int):
            return curr
        curr = curr.right


def test_explode1():
    example1 = [[[[[9, 8], 1], 2], 3], 4]
    exploded1 = [[[[0, 9], 2], 3], 4]
    assert SFNum(example1).find().pair() == (9, 8)
    assert SFNum(example1).explode().arr() == exploded1


def test_explode2():
    example2 = [7, [6, [5, [4, [3, 2]]]]]
    exploded2 = [7, [6, [5, [7, 0]]]]
    assert SFNum(example2).find().pair() == (3, 2)
    assert SFNum(example2).explode().arr() == exploded2


def test_explode3():
    example3 = [[6, [5, [4, [3, 2]]]], 1]
    exploded3 = [[6, [5, [7, 0]]], 3]
    assert SFNum(example3).find().pair() == (3, 2)
    assert SFNum(example3).explode().arr() == exploded3


def test_explode4():
    example4 = [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]
    exploded4 = [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    assert SFNum(example4).find().pair() == (7, 3)
    assert SFNum(example4).explode().arr() == exploded4
    exploded4p2 = [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    assert SFNum(example4).reduce().arr() == exploded4p2


def test_explode5():
    example5 = [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    exploded5 = [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    assert SFNum(example5).find().pair() == (3, 2)
    assert SFNum(example5).explode().arr() == exploded5


def test_split_pair():
    assert SFNum([10, 0]).reduce().arr() == [[5, 5], 0]


def test_sample():
    # after addition:
    num = SFNum([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    assert num.explode().arr() == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
    assert num.explode().arr() == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
    assert num.split().arr() == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]
    assert num.split().arr() == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    assert num.explode().arr() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    num = SFNum([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    num.add([1, 1])
    assert num.arr() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def test_reduce():
    num = SFNum([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    num.reduce()
    assert num.arr() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def test_wtf():
    r = [[[[[1, 1], [2, 2]], [3, 3]], [4, 4]], [5, 5]]
    num = SFNum(r)
    assert num.arr() == r
    p = num.find()
    assert p.pair() == (1, 1)
    assert p.depth == 4
    assert num.reduce().arr() == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]


def test_simple():
    num = SFNum([1, 1])
    assert num.add([2, 2]).arr() == [[1, 1], [2, 2]]
    assert num.add([3, 3]).arr() == [[[1, 1], [2, 2]], [3, 3]]
    assert num.add([4, 4]).arr() == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
    assert num.reduce().arr() == [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
    assert num.add([5, 5]).arr() == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
    assert num.add([6, 6]).arr() == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]


def test_larger():
    numbers = read('day18-larger.txt')
    assert numbers[0] == [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]
    assert numbers[1] == [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]

    num = SFNum(numbers[0])
    num.reduce()

    num.add(numbers[1])
    assert num.arr() == [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]],
                         [[8, [7, 7]], [[7, 9], [5, 0]]]]

    num.add(numbers[2])
    assert num.arr() == [[[[6, 7], [6, 7]], [[7, 7], [0, 7]]],
                         [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]

    num.add(numbers[3])
    assert num.arr() == [[[[7, 0], [7, 7]], [[7, 7], [7, 8]]],
                         [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]

    num.add(numbers[4])
    assert num.arr() == [[[[7, 7], [7, 8]], [[9, 5], [8, 7]]],
                         [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]

    num.add(numbers[5])
    assert num.arr() == [[[[6, 6], [6, 6]], [[6, 0], [6, 7]]],
                         [[[7, 7], [8, 9]], [8, [8, 1]]]]

    num.add(numbers[6])
    assert num.arr() == [[[[6, 6], [7, 7]], [[0, 7], [7, 7]]],
                         [[[5, 5], [5, 6]], 9]]

    num.add(numbers[7])
    assert num.arr() == [[[[7, 8], [6, 7]], [[6, 8], [0, 8]]],
                         [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]

    num.add(numbers[8])
    assert num.arr() == [[[[7, 7], [7, 7]], [[8, 7], [8, 7]]],
                         [[[7, 0], [7, 7]], 9]]
    num.add(numbers[9])
    assert num.arr() == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]],
                         [[[0, 7], [6, 6]], [8, 7]]]


def test_homework():
    numbers = read('day18-sample.txt')
    num = SFNum(numbers[0])
    num.reduce()
    for addition in numbers[1:]:
        num.add(addition)

    result = [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]],
              [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]

    assert num.arr() == result

    assert num.magnitude() == 4140


def test_magnitude():
    assert SFNum([[1, 2], [[3, 4], 5]]).magnitude() == 143
    assert SFNum([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]).magnitude() == 1384
    assert SFNum([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]).magnitude() == 445
    assert SFNum([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]).magnitude() == 791
    assert SFNum([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]).magnitude() == 1137
    assert SFNum([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]],
                  [[[0, 7], [6, 6]], [8, 7]]]).magnitude() == 3488


def test_input():
    numbers = read('day18-input.txt')
    num = SFNum(numbers[0])
    num.reduce()
    for addition in numbers[1:]:
        num.add(addition)
    assert num.magnitude() == 2501


def max_of_two(numbers) -> int:
    candidates, maximum = list(permutations(numbers, 2)), 0
    for x, y in candidates:
        mag = SFNum(x).add(y).magnitude()
        maximum = max(maximum, mag)
    return maximum


def test_max_of_two():
    numbers = read('day18-sample.txt')
    assert max_of_two(numbers) == 3993

    numbers = read('day18-input.txt')
    assert max_of_two(numbers) == 4935
