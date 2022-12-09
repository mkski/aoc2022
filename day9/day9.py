from collections import namedtuple
from math import sqrt

inputs = open("input").read().split("\n")
Point = namedtuple("point", ("x", "y"))

d = {
    "R": 1,
    "U": 1,
    "D": -1,
    "L": -1
}

direct = {
    "R": 0,
    "L": 0,
    "U": 1,
    "D": 1
}

def distance(p1, p2):
    return int(sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2))


def move_head(h, direction, dist):
    if direct[direction] == 0:
        return Point(h.x + dist * d[direction], h.y)
    else:
        return Point(h.x, h.y + dist * d[direction])


def move_tail(h, t):
    if h.x - t.x >= 2 and h.y == t.y:
        return Point(t.x + 1, t.y)
    elif h.y - t.y >= 2 and h.x == t.x:
        return Point(t.x, t.y + 1)
    elif h.x - t.x >= -2 and h.y == t.y:
        return Point(t.x - 1, t.y)
    elif h.y - t.y >= -2 and h.x == t.x:
        return Point(t.x, t.y - 1)
    elif h.x > t.x and h.y > t.y:
        return Point(t.x + 1, t.y + 1)
    elif h.x < t.x and h.y > t.y:
        return Point(t.x - 1, t.y + 1)
    elif h.x > t.x and h.y < t.y:
        return Point(t.x + 1, t.y - 1)
    elif h.x < t.x and h.y < t.y:
        return Point(t.x - 1, t.y - 1)


head = tail = Point(0, 0)

positions = []
for move in inputs:
    direction, dist = move.split()
    for i in range(1, int(dist)+1):
        head = move_head(head, direction, 1)
        if distance(head, tail) >= 2:
            tail = move_tail(head, tail)
            if tail not in positions:
                positions.append(tail)

print(len(positions))

snake = [Point(0, 0)] * 10
positions = set()
for move in inputs:
    direction, dist = move.split()
    for i in range(1, int(dist)+1):
        snake[0] = move_head(snake[0], direction, 1)
        for p in range(1, len(snake)):
            if distance(snake[p-1], snake[p]) >= 2:
                snake[p] = move_tail(snake[p-1], snake[p])
                if p == len(snake) - 1:
                    positions.add(snake[p])

print(len(positions))