
import re


def read(s):
    s = s[15:]
    tx0, tx1, ty0, ty1 = [int(i) for i in re.split(', y=|\\.\\.', s)]

    min_tx = min(tx0, tx1)
    max_tx = max(tx0, tx1)
    max_ty = max(ty0, ty1)
    min_ty = min(ty0, ty1)

    return (min_tx, max_tx, max_ty, min_ty)


class Probe:
    def __init__(self, target) -> None:
        self.target = target  # tx0, tx1, ty0, ty1

    def bf(self):
        _, tx1, _, ty1 = self.target

        best_y = 0
        hits = 0
        for ivx in range(1, tx1 + 1):
            for ivy in range(ty1, 1000):  # XXX: ivy max 1000 likely not right?
                x, y, vx, vy = 0, 0, ivx, ivy
                max_y = 0
                tracking = self.on_target(x, y)
                step = 0
                while tracking == -1 and step < 10000:  # XXX max steps 10000 may not be enough?
                    step += 1
                    x, y, vx, vy = self.f(x, y, vx, vy)
                    max_y = max(max_y, y)
                    tracking = self.on_target(x, y)
                if tracking == -1:
                    raise ValueError('ininite loop?')
                if tracking == 0:
                    hits += 1
                    if max_y > best_y:
                        print(
                            f'velocity {(ivx,ivy)} hit target with max y={max_y} step={step}')
                        best_y = max_y
                # if tracking == 1:
                #     print(f'velocity {(ivx,ivy)} overshot')
        return (best_y, hits)

    def on_target(self, x, y) -> int:
        """returns -1 if tracking, 0 if on target and 1 if overshot"""
        tx0, tx1, ty0, ty1 = self.target
        if x > tx1 or y < ty1:
            return 1
        if x >= tx0 and y <= ty0:
            return 0
        return -1

    def f(self, x, y, vx, vy, steps=1):
        for _ in range(steps):
            x += vx
            y += vy
            vx = max(vx - 1, 0)  # FUTURE: can increase to zero from neg
            vy += -1
        return (x, y, vx, vy)


def test_sample():
    sample = 'target area: x=20..30, y=-10..-5'
    target = read(sample)
    assert target == (20, 30, -5, -10)

    probe = Probe(target)
    assert probe.f(0, 0, 7, 2, steps=1) == (7, 2, 6, 1)
    assert probe.f(0, 0, 7, 2, steps=2) == (13, 3, 5, 0)
    assert probe.f(0, 0, 7, 2, steps=3) == (18, 3, 4, -1)
    assert probe.f(0, 0, 7, 2, steps=7) == (28, -7, 0, -5)
    assert probe.f(0, 0, 7, 2, steps=8) == (28, -12, 0, -6)

    assert probe.on_target(0, 0) == -1
    assert probe.on_target(28, -7) == 0
    assert probe.on_target(28, -12) == 1

    assert probe.bf() == (45, 112)


def test_bf():
    probe = Probe(read('target area: x=57..116, y=-198..-148'))
    assert probe.bf() == (19503, 5200)
