from queue import PriorityQueue
from pathlib import Path


def read(filename: str) -> list[list[str]]:
    filename = Path(__file__).parent / filename
    with open(filename, encoding='utf-8') as f:
        return [list(l) for l in f.read().splitlines(keepends=False)]


def find_2d(key: str, heightmap: list[list[str]]) -> tuple[int, int]:
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j] == key:
                return (i, j)
    return (-1, -1)


def find_all_2d(key: str, heightmap: list[list[str]]) -> list[tuple[int, int]]:
    result = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j] == key:
                result.append((i, j))
    return result


def find_path(graph, start, end, last) -> int:
    """
    Dijkstra's Algorithm Steps
    0. The starting node is considered to be solved
    1. Identify all unsolved nodes that are connected to any solved node
    2. For each line connecting a solved node to a unsolved node, calculate the candidate cost. A candidate is an unsolved node.
    3. Choose the candidate with the smallest cost. If there is a tie, then chose one arbitrarily.
    4. Change the smallest candidate status to solved from unsolved.
    5. Add the line to the set keeping track of that path.
    6. Repeat steps 1-5 until we have reached the destination node.
    """

    dist, visited, shortest, pq = 0, {}, {}, PriorityQueue()

    for vertex, _ in graph.items():
        shortest[vertex] = float('inf')

    visited[start] = True
    shortest[start] = dist
    pq.put((0, start))

    print()

    while not pq.empty():
        (dist, curr_pos) = pq.get()
        visited[curr_pos] = True

        for neighbor in get_neighbors(curr_pos, last):
            delta = ord(graph[neighbor]) - ord(graph[curr_pos])
            if delta > 1:
                # print(
                # f'{graph[curr_pos]} skip {graph[neighbor]} because {delta=:2} {curr_pos} > {neighbor}')
                continue

            # cost_of_neighbor = graph[neighbor]
            cost_of_neighbor = 1
            if neighbor not in visited:
                # print(
                # f'{graph[curr_pos]} try  {graph[neighbor]} because {delta=:2} {curr_pos} > {neighbor}')
                old_cost = shortest[neighbor]
                new_cost = shortest[curr_pos] + cost_of_neighbor
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    shortest[neighbor] = new_cost

    return shortest[end]


def get_neighbors(pos: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    row, col = pos
    end_row, end_col = end
    result = []
    if row > 0:
        result.append((row-1, col))
    if col > 0:
        result.append((row, col-1))
    if row < end_row:
        result.append((row+1, col))
    if col < end_col:
        result.append((row, col+1))
    return result


def sol1(heightmap: list[list[str]]) -> int:
    start = find_2d('S', heightmap)
    end = find_2d('E', heightmap)
    graph = {}
    for row, cols in enumerate(heightmap):
        for col, height in enumerate(cols):
            pos = (row, col)
            graph[pos] = height

    last = (len(heightmap)-1, len(heightmap[0])-1)

    graph[start] = chr(ord('a'))
    graph[end] = chr(ord('z')+1)

    shortest_path = find_path(graph, start, end, last)

    return shortest_path


def sol2(heightmap: list[list[str]]) -> int:
    end = find_2d('E', heightmap)
    start = find_2d('S', heightmap)
    starts = find_all_2d('a', heightmap)
    starts.append(start)

    graph = {}
    for row, cols in enumerate(heightmap):
        for col, height in enumerate(cols):
            pos = (row, col)
            graph[pos] = height

    last = (len(heightmap)-1, len(heightmap[0])-1)

    graph[start] = chr(ord('a'))
    graph[end] = chr(ord('z')+1)

    shortest_path = min([
        find_path(graph, start, end, last) for start in starts
    ])

    return shortest_path


def test_sample():
    heightmap = read('day12-sample.txt')
    assert sol1(heightmap) == 31
    assert sol2(heightmap) == 29


def test_sol():
    heightmap = read('day12-input.txt')
    assert sol1(heightmap) == 383
    assert sol2(heightmap) == 377
