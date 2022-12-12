from operator import ge, le
from copy import deepcopy

inputs = open("in").read().split("\n")


class Node:

    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

        if self.value == "S":
            self.elevation = ord("a")
        elif self.value == "E":
            self.elevation = ord("z")
        else:
            self.elevation = ord(self.value)

        self.neighbors = set()

    def add_neighbor(self, node):
        self.neighbors.add(node)

    def __hash__(self):
        return hash((self.row, self.col))

    def __str__(self):
        return f"Node({self.row}, {self.col}, {chr(self.elevation)}({self.elevation}))"

    def __repr__(self):
        return self.__str__()

    def __sub__(self, other):
        return self.elevation - other.elevation

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)


node_map = [
    [Node(r, c, col) for c, col in enumerate(row)]
    for r, row in enumerate(inputs)
]

N_ROWS = len(node_map)
N_COLS = len(node_map[0])


def add_neighbors(node, node_map, reverse=False):
    r, c = node.row, node.col
    target = 1 if reverse else -1
    op = {
        True: le,
        False: ge
    }[reverse]

    if r - 1 >= 0 and op(node_map[r][c] - node_map[r-1][c], target):
        node.add_neighbor(node_map[r-1][c])

    if r + 1 < N_ROWS and op(node_map[r][c] - node_map[r+1][c], target):
        node.add_neighbor(node_map[r+1][c])

    if c - 1 >= 0 and op(node_map[r][c] - node_map[r][c-1], target):
        node.add_neighbor(node_map[r][c-1])

    if c + 1 < N_COLS and op(node_map[r][c] - node_map[r][c+1], target):
        node.add_neighbor(node_map[r][c+1])


def build_graph(node_map, reverse=False):
    nodes = []
    start_node = end_node = None
    for r, row in enumerate(node_map):
        for c, node in enumerate(row):
            if node.value == "S":
                start_node = node
            elif node.value == "E":
                end_node = node

            add_neighbors(node, node_map, reverse=reverse)
            nodes.append(node)
    return nodes, start_node, end_node


def shortest_path(nodes, start, end=None):
    distances = {}
    previous = {}
    queue = set()

    for node in nodes:
        distances[node] = 9999999
        previous[node] = None
        queue.add(node)

    distances[start] = 0

    while len(queue):
        node = min([n for n in queue], key=lambda x: distances[x])
        queue.remove(node)

        if end and node.value == end.value:
            break

        for neighbor in node.neighbors:
            if neighbor not in queue:
                continue
            alt = distances[node] + 1
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = node
    
    if end:
        return distances[end]
    else:
        return min(d for n, d in distances.items() if n.value == "a")


nodes, start, end = build_graph(deepcopy(node_map))
print(shortest_path(nodes, start, end))

nodes, start, end = build_graph(deepcopy(node_map), reverse=True)
print(shortest_path(nodes, end))
