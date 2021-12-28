from __future__ import annotations
from copy import copy
from typing import Type, List


# AMBER, BRONZE, COPPER, DESERT, FREE, INVALID
A, B, C, D = 'A', 'B', 'C', 'D'
ENERGY = {A: 1, B: 10, C: 100, D: 1000}
TARGETS = {A: 0, B: 1, C: 2, D: 3}
GOAL = 'ABCD'
HALL = '..0.1.2.3..'


class State:
    #############
    #..!.!.!.!..#
    ###B#C#B#D###
    # #A#D#C#A#
    # #########
    #
    # four rooms
    # must sort left by room
    # least total energy
    # must move in one fluid movement out, and then one fluid movement back in
    # cannot block a room
    # must double move when leaving room
    # cannot enter non-dest room
    # cannot enter dest room if occupied by another kind
    # cannot move within hallway
    def __init__(self, hall, rooms, energy=0) -> None:
        self.hall = hall
        self.rooms = rooms
        while len(self.rooms) < 4:
            self.rooms += [GOAL]
        self.energy = energy
        self.last = None
        self.prev = None

    def __repr__(self) -> str:
        last = self.last if self.last is not None else 'none'
        return f"State('{self.hall}', {self.rooms}, {self.energy:6d}, '{last:20s}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.energy == other.energy and self.hall == other.hall and \
                self.rooms == other.rooms
        return False

    def solved(self):
        return all(layer == GOAL for layer in self.rooms)

    def fork(self, src, i: int, dst, j: int, inc: int) -> State:
        hall = self.hall
        rooms = copy(self.rooms)

        if src == -1:
            mover = hall[i]
            hall = hall[:i] + '.' + hall[i + 1:]
        else:
            mover = rooms[src][i]
            rooms[src] = rooms[src][:i] + '.' + rooms[src][i+1:]

        if dst == -1:
            hall = hall[:j] + mover + hall[j + 1:]
        else:
            rooms[dst] = rooms[dst][:j] + mover + rooms[dst][j+1:]

        state = State(hall, rooms, self.energy+inc)
        state.last = f'{src}[{i:2d}]={mover} to {dst}[{j:2d}]'
        state.prev = self
        return state

    def debug(self):
        if self.prev is None:
            result = 'starting state:'
            energy = ''
        else:
            result = self.prev.debug()
            energy = f' using: {(self.energy - self.prev.energy):6d}'
        return result + "\n" + self.__repr__() + energy


def left_of(r):
    a = [0, 1, 3, 5, 7, 9, 10]
    return reversed(a[:r+2])


def right_of(r):
    a = [0, 1, 3, 5, 7, 9, 10]
    return iter(a[r+2:])


def test_iters():
    assert list(left_of(0)) == [1, 0]
    assert list(left_of(3)) == [7, 5, 3, 1, 0]
    assert list(right_of(0)) == [3, 5, 7, 9, 10]
    assert list(right_of(3)) == [9, 10]


def path_free(r1, r2, hall) -> int:
    r1, r2 = [2, 4, 6, 8][min(r1, r2)], [2, 4, 6, 8][max(r1, r2)]
    for h in range(r1+1, r2, 2):
        if hall[h] != '.':
            return 0
    return r2-r1


def hall_free(h1, r, hall) -> int:
    h2 = (2, 4, 6, 8)[r]
    # h1 may be 0 or 10
    # h2 is always above a room
    h1, h2 = min(h1, h2), max(h1, h2)
    for h in range(h1+1, h2, 1):
        if h in (2, 4, 6, 8):
            continue
        if hall[h] != '.':
            return 0
    return h2-h1


def reversed_enumerate(collection: list):
    for i in range(len(collection)-1, -1, -1):
        yield i, collection[i]


def next_state(state: Type[State]) -> List[State]:
    start = None
    while True:
        # type 1 of 3 hall -> room (guaranteed shortest)
        for h in [0, 1, 3, 5, 7, 9, 10]:
            if state.hall[h] != '.':
                state = move_hall_to_room(state, h)

        # type 2 of 3 room -> room (guaranteed shortest)
        for r in range(4):
            state = move_room_to_room(state, r)

        if start == state:
            # no sense generating possibilities until
            # all guaratnees are implemented
            break
        start = state

    if state.solved():
        return [state]

    # type 3 of 3 room -> hall (multiple possibilities)
    return move_room_to_hall(state)


def move_room_to_hall(state: Type[State]) -> List[State]:
    hall = state.hall
    moves = []
    for r in range(4):
        if all(layer[r] in ['.', GOAL[r]] for layer in state.rooms):
            continue
        # 8 sub-types (top/mid1/mid2/bot and left/right)
        for depth, layer in enumerate(state.rooms):
            if layer[r] == '.':
                continue
            mover = layer[r]
            for c, h in enumerate(left_of(r), 1):
                if hall[h] != '.':
                    break
                c = c*2 + depth
                if h in (0, 10):
                    c -= 1
                moves.append(state.fork(depth, r, -1, h, c * ENERGY[mover]))
            for c, h in enumerate(right_of(r), 1):
                if hall[h] != '.':
                    break
                c = c*2 + depth
                if h in (0, 10):
                    c -= 1
                moves.append(state.fork(depth, r, -1, h, c * ENERGY[mover]))
            break
    return moves


def move_room_to_room(state: Type[State], r) -> Type[State]:
    for src_depth, layer in enumerate(state.rooms):
        if layer[r] == '.':
            continue
        mover = layer[r]
        dst = TARGETS[mover]
        if dst == r:
            return state
        for dst_depth, dst_layer in reversed_enumerate(state.rooms):
            if dst_layer[dst] == mover:
                continue
            if dst_layer[dst] != '.':
                return state  # dst not free
            c = path_free(r, dst, state.hall)
            if c > 0:  # we can slip into room
                c += src_depth + dst_depth + 2
                return state.fork(src_depth, r, dst_depth, dst, c * ENERGY[mover])
            return state
    return state


def move_hall_to_room(state: Type[State], h) -> Type[State]:
    mover = state.hall[h]
    dst = TARGETS[mover]
    for dst_depth, dst_layer in reversed_enumerate(state.rooms):
        if dst_layer[dst] == mover:
            continue
        if dst_layer[dst] != '.':
            return state
        c = hall_free(h, dst, state.hall)
        if c > 0:  # we can slip into room
            c += dst_depth + 1
            return state.fork(-1, h, dst_depth, dst, c * ENERGY[mover])
        return state
    return state


def looper(start, least=float('inf')):
    states = [start]
    best = None
    print()
    while len(states) > 0 and len(states) < 1_000_000:
        state = states.pop()

        if state.energy >= least:
            continue

        new_states = next_state(state)

        if len(new_states) == 1:
            if new_states[0].energy < least and new_states[0].solved():
                print(f'{new_states[0]} new least')
                least = new_states[0].energy
                best = new_states[0]
                continue

        states += new_states

    assert len(states) == 0
    return best


def test_path_free():
    assert path_free(0, 1, '..0A1.2.3..') == 0
    assert path_free(0, 1, '..0.1.2.3..') == 2


def test_hall_free():
    assert hall_free(5, 3, '..0.1D2.3A.') == 3
    assert hall_free(0, 3, 'A.0.1.2.3..') == 8
    assert hall_free(10, 0, '..0.1.2.3.A') == 8
    assert hall_free(2, 3, '..0.1.2B3B.') == 0
    assert hall_free(2, 0, '.B0.1.2.3..') == 0
    assert hall_free(0, 3, 'A.0.1B2.3..') == 0
    assert hall_free(10, 0, '..0.1B2.3.A') == 0


def test_first_move():
    state = State('..0B1D2.3..', ['B.CD', 'A.CA'])
    # the 2 b's slide into room1
    moves = next_state(state)
    assert len(moves) == 3


def test_second_move():
    state = State('..0.1D2D3A.', ['.BC.', 'ABC.'])
    moves = next_state(state)
    assert len(moves) == 1


def test_looper():
    state = State('..0B1D2.3..', ['B.CD', 'A.CA'],
                  12521 - 30 - 40 - 2000 - 3 - 7000 - 8)
    best = looper(state, 30_000)
    assert best.energy == 12521, best.debug()

    state = State('..0.1D2D3A.', ['.BC.', 'ABC.'], 12521 - 7000 - 8)
    best = looper(state, 30_000)
    assert best.energy == 12521, best.debug()

    state = State('..0.1.2.3A.', ['.BCD', 'ABCD'], 12521 - 8)
    best = looper(state, 30_000)
    assert best.energy == 12521, best.debug()


def test_slider():
    best = looper(State('AB0.1.2.3CD', ['....', 'ABCD']))
    assert best.energy == 3443, best.debug()


def test_next_state():
    assert len(next_state(State('..0.1.2.3..', ['DBCA', 'ABCD']))) == 14


def test_cost():
    states = move_room_to_hall(State('..0A1.2.3..', ['B.CD', 'ABCD']))
    assert len(states) == 2
    assert states[0] == State('.B0A1.2.3..', ['..CD', 'ABCD'], energy=20)
    assert states[1] == State('B.0A1.2.3..', ['..CD', 'ABCD'], energy=30)

    states = move_room_to_hall(State('..0.1D2.3..', ['.BCD', 'ABCA']))
    assert states[0] == State('..0.1D2D3..', ['.BC.', 'ABCA'], energy=2000)

    states = move_room_to_hall(State('..0.1D2D3..', ['.BC.', 'ABCA']))
    assert states[0] == State('..0.1D2D3A.', ['.BC.', 'ABC.'], energy=3)
    assert states[1] == State('..0.1D2D3.A', ['.BC.', 'ABC.'], energy=4)

    states = move_room_to_room(State('AA0.1.2.3BB', ['..C.', 'DDC.']), 0)
    assert states == State('AA0.1.2.3BB', ['..C.', '.DCD'], energy=10_000)


def test_passing():
    assert len(next_state(State(HALL, ['ABCD', 'ABCD']))) == 1
    assert len(next_state(State('..0A1.2.3..', ['B.CD', 'ABCD']))) == 2
    assert len(next_state(State('.A0.1.2.3..', ['B.CD', 'ABCD']))) == 1
    assert len(next_state(State('A.0.1.2.3..', ['B.CD', 'ABCD']))) == 1
    assert len(next_state(State('..0.1.2.3.A', ['B.CD', 'ABCD']))) == 1
    assert len(next_state(State('..0B1.2.3..', ['AC.D', 'ABCD']))) == 1
    assert len(next_state(State('.B0.1.2.3..', ['AC.D', 'ABCD']))) == 1
    assert len(next_state(State('B.0.1.2.3..', ['AC.D', 'ABCD']))) == 1
    assert len(next_state(State('..0.1.2.3.B', ['AC.D', 'ABCD']))) == 1
    assert len(next_state(State('AA0.1.2.3BB', ['..C.', 'DDC.']))) == 1

    assert len(next_state(State('A.0.1.2.3..', ['.BCD', 'ABCD']))) == 1


def test_sample():
    best = looper(State(HALL, ['BCBD', 'ADCA']))
    assert best.energy == 12521, best.debug()


def test_input():
    best = looper(State(HALL, ['DACC', 'DABB']))
    assert best.energy == 19046, best.debug()


def test_sample_2():
    best = looper(State(HALL, ['BCBD', 'DCBA', 'DBAC', 'ADCA']))
    assert best.energy == 44169, best.debug()


def test_input_2():
    best = looper(State(HALL, ['DACC', 'DCBA', 'DBAC', 'DABB']))
    assert best.energy == 47484, best.debug()
