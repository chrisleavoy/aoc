import re
from dataclasses import dataclass
from pathlib import Path
from queue import PriorityQueue
from typing import Self

import matplotlib.pyplot as plt
import networkx as nx


@dataclass
class Node:
    name: str
    rate: int
    peers: dict[str, Self]

    def pp(self) -> str:
        return self.name if self.rate == 0 else str(self.rate)

    def __hash__(self):
        return hash(self.name)


def parse(line: str, nodes):
    r = re.compile(
        r'Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)')

    m = r.match(line)
    if m is None:
        raise ValueError(f'{line=}')

    g = m.groups()
    name, rate, peers = g[0], int(g[1]), g[2].split(', ')

    node = nodes.get(name, None)
    if node is None:
        node = Node(name, rate, dict())
        nodes[name] = node
    node.rate = rate

    for peer_name in peers:
        peer = nodes.get(peer_name, None)
        if peer is None:
            peer = Node(peer_name, rate, dict())
            nodes[peer.name] = peer
        node.peers[peer.name] = peer
        peer.peers[node.name] = node

    return node


def read(filename: str) -> list[Node]:
    path = Path(__file__).parent.joinpath(filename)
    nodes = {}
    with open(path, encoding='utf-8') as f:
        return [parse(line, nodes) for line in f.read().splitlines()]


class GraphVisualization:
    def __init__(self):
        self.visual = []

    def add_edge(self, a, b):
        self.visual.append([a, b])

    def visualize(self):
        g = nx.Graph()
        g.add_edges_from(self.visual)
        nx.draw_networkx(g)
        plt.show()


def find_path(nodes: dict[str, Node], start: Node, end: Node) -> float | int:
    dist, visited, shortest, pq = 0, dict[str, bool](
    ), dict[str, float | int](), PriorityQueue()

    for _, node in nodes.items():
        shortest[node.name] = float('inf')

    visited[start.name] = True
    shortest[start.name] = dist
    pq.put((0, start.name))

    while not pq.empty():
        (dist, curr_pos) = pq.get()
        visited[curr_pos] = True

        node = nodes[curr_pos]
        for neighbor in node.peers.keys():
            cost_of_neighbor = 1
            if neighbor not in visited:
                old_cost = shortest[neighbor]
                new_cost = shortest[curr_pos] + cost_of_neighbor
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    shortest[neighbor] = new_cost

    return shortest[end.name]


def test_sol1():
    nodes = read('day16-input.txt')

    rates = [node.rate for node in nodes if node.rate > 0]
    rates.sort(reverse=True)
    assert rates == [25, 24, 23, 22, 20, 17, 15, 11, 10, 9, 7, 6, 5, 4, 3]

    rate_dict = dict([(node.rate, node.name)
                     for node in nodes if node.rate > 0])
    node_dict = dict([(node.name, node) for node in nodes])

    assert find_path(node_dict, node_dict['AA'], node_dict['GK']) == 1
    assert find_path(node_dict, node_dict['AA'], node_dict['GD']) == 2

    # for rate, node_name in rate_dict.items():

    graph = nx.Graph()
    for node in nodes:
        for _, peer in node.peers.items():
            graph.add_edge(node.pp(), peer.pp())
    # edges = [
    #     (node.pp(), peer.pp()) for node in nodes
    # ]
    # graph.add_edges_from(edges)
    nx.draw_networkx(graph)
    plt.show()

# def test_sol2():
