from queue import PriorityQueue


def read(filename: str):
    grid = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            row = [int(x) for x in line.strip()]
            grid.append(row)
    return grid


def sol1(grid) -> int:
    graph = {}
    for row, cols in enumerate(grid):
        for col, risk in enumerate(cols):
            pos = (row, col)
            graph[pos] = risk
    end = pos
    return find_path(graph, end)


def find_path(graph, end) -> int:
    """
    Dijkstra’s Algorithm Steps
    0. The starting node is considered to be solved
    1. Identify all unsolved nodes that are connected to any solved node
    2. For each line connecting a solved node to a unsolved node, calculate the candidate cost. A candidate is an unsolved node.
    3. Choose the candidate with the smallest cost. If there is a tie, then chose one arbitrarily.
    4. Change the smallest candidate status to solved from unsolved.
    5. Add the line to the set keeping track of that path.
    6. Repeat steps 1–5 until we have reached the destination node.
    """

    start, dist, visited, shortest, pq = (0, 0), 0, {}, {}, PriorityQueue()

    for vertex, _ in graph.items():
        shortest[vertex] = float('inf')

    visited[start] = True
    shortest[start] = dist
    pq.put((0, start))

    while not pq.empty():
        (dist, curr_pos) = pq.get()
        visited[curr_pos] = True

        for neighbor in get_neighbors(curr_pos, end):
            risk_of_neighbor = graph[neighbor]
            if neighbor not in visited:
                old_cost = shortest[neighbor]
                new_cost = shortest[curr_pos] + risk_of_neighbor
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    shortest[neighbor] = (new_cost, curr_pos)

    return shortest[end]


def get_neighbors(pos, end):
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


def sol2(grid):
    n = len(grid)
    m = len(grid[0])

    expanded = []
    for row in range(n*5):
        expanded.append([-1]*(m*5))

    for row, cols in enumerate(grid):
        for col, risk in enumerate(cols):
            for x in range(5):
                for y in range(5):
                    risk = grid[row][col] + x + y
                    if risk > 9:
                        risk -= 9
                    r = row+y*n
                    c = col+x*m
                    expanded[r][c] = risk
    return sol1(expanded)


def test_neighbors():
    assert get_neighbors((0, 0), (1, 1)) == [(1, 0), (0, 1)]
    assert get_neighbors((1, 1), (1, 1)) == [(0, 1), (1, 0)]


def test_find_path():
    assert sol1(read('day15-sample.txt')) == 40
    assert sol1(read('day15-input.txt')) == 652


def test_sol2():
    assert sol2(read('day15-sample.txt')) == 315
    assert sol2(read('day15-input.txt')) == 2938
