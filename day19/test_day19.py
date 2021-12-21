from __future__ import annotations
from pathlib import Path
from typing import Type, Set, List, Mapping, Tuple
from itertools import permutations, product


class Point:
    def __init__(self, x: int, y: int, z: int):
        self.x, self.y, self.z = x, y, z

    def offset(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def shift(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: Type[Point]) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f'({self.x:5d}, {self.y:5d}, {self.z:5d})'

    def manhattan_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def distance_to(self, other: Type[Point]) -> float:
        x1, x2, y1, y2 = self.x, other.x, self.y, other.y
        # return (((x2 - x1)**2) + ((y2-y1)**2))**0.5 # w/o z
        z1, z2 = self.z, other.z
        return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5


class Scan:
    def __init__(self):
        self.beacons: Set[Point] = set()
        self.distances: Mapping[float, List[Set[Point]]] = []
        self.offset = Point(0, 0, 0)

    def add(self, x, y, z):
        self.beacons.add(Point(x, y, z))
        return self

    def distance_set(self) -> Set[float]:
        if len(self.distances) == 0:
            self.compute_distances()
        return set(self.distances.keys())

    def compute_distances(self) -> Mapping[float, List[Set[Point]]]:
        self.distances: Mapping[float, List[Set[Point]]] = {}
        beacons = list(self.beacons)
        for i, pos1 in enumerate(beacons[:-1]):
            for _, pos2 in enumerate(beacons[i+1:]):
                dist = pos1.distance_to(pos2)
                Points = self.distances.get(dist)
                if Points is None:
                    Points = [{pos1, pos2}]
                    self.distances[dist] = Points
                else:
                    Points.append({pos1, pos2})
        return self.distances

    def rotations(self) -> List[List[Point]]:
        """ return a list of all possible rotations of the beacons list """
        result = []
        for rotation in rotation_permutations():
            x, xsign, y, ysign, z, zsign = rotation
            points = []
            for point in self.beacons:
                lookup = {'x': point.x, 'y': point.y, 'z': point.z}
                p = Point(lookup[x]*xsign, lookup[y]*ysign, lookup[z]*zsign)
                points.append(p)
            result.append(points)
        return result

    def overlapping(self, other: Type[Scan]) -> Tuple[bool, Tuple[int], List[Point]]:
        for rotation in other.rotations():
            counts = {}
            for point1 in rotation:
                for point2 in self.beacons:
                    offset = point2.offset(point1)
                    counts[offset] = 1 + counts.get(offset, 0)
            for offset, count in counts.items():
                if count >= 12:
                    print(f'found overlap with offset {offset}')
                    return True, offset, rotation
        return False, None, None

    def merge(self, beacons: List[Point], offset):
        if self.offset != Point(0, 0, 0):
            raise ValueError('can only merge once')
        self.offset = offset
        for point in beacons:
            self.beacons.add(point.shift(offset))
        return self


def rotation_permutations() -> List(tuple):
    """ return a list of (x, xsign, y, ysign, z, zsign) """
    result = []
    for axis in permutations(['x', 'y', 'z']):
        for signs in product([-1, 1], repeat=3):
            rotation = (axis[0], signs[0],
                        axis[1], signs[1],
                        axis[2], signs[2])
            result.append(rotation)
    return result


def locate_scanners(scans) -> List[Scan]:
    located = {0: scans[0]}
    while len(located) < len(scans):
        for i, unresolved in enumerate(scans):
            if i in located:
                continue
            for _, resolved in located.items():
                overlap, offset, points = resolved.overlapping(unresolved)
                if overlap:
                    scan = Scan().merge(points, offset)
                    located[i] = scan
                    break
    return located.values()


def read(filename: str):
    filename = Path(__file__).parent / filename
    scans: List[Scan] = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('---'):
                scan = Scan()
                scans.append(scan)
            elif line != '\n':
                v = [int(i) for i in line.strip().split(',')]
                scan.add(*v)
    return scans


def largest_manhattan_dist(scans: List[Scan]) -> int:
    scans = list(scans)
    largest = -1
    for i, scan1 in enumerate(scans[:-1]):
        for scan2 in scans[i+1:]:
            largest = max(largest, scan1.offset.manhattan_dist(scan2.offset))
    return largest


def test_sample():
    scans = read('day19-sample.txt')
    scans = locate_scanners(scans)
    result = Scan()
    for scan in scans:
        for beacon in scan.beacons:
            result.beacons.add(beacon)
    assert len(result.beacons) == 79
    assert largest_manhattan_dist(scans) == 3621


def test_input():
    scans = read('day19-input.txt')
    scans = locate_scanners(scans)
    result = Scan()
    for scan in scans:
        for beacon in scan.beacons:
            result.beacons.add(beacon)
    assert len(result.beacons) == 383
    assert largest_manhattan_dist(scans) == 9854


def test_rotation_permutations():
    r = rotation_permutations()
    print(r)
    assert len(r) == 48
