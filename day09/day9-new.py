from collections import namedtuple
from math import sqrt

inputs = open("in").read().split("\n")
Point = namedtuple("Point", ("x", "y"))

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


def translate(p, x, y):
    return Point(p.x + x, p.y + y)


def move(p, direction):
    if direct[direction] == 0:
        return Point(p.x + d[direction], p.y)
    else:
        return Point(p.x, p.y + d[direction])


def distance(p1, p2):
    return int(sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2))


def get_move_xy(p1, p2):
    return (
        1 if p1.x > p2.x else
        -1 if p1.x < p2.x else
        0,
        1 if p1.y > p2.y else
        -1 if p1.y < p2.y else
        0
    )


def move_snake(moves, length):
    snake = [Point(0, 0)] * length

    positions = set()
    for m in moves:
        direction, dist = m.split()

        for _ in range(int(dist)):
            snake[0] = move(snake[0], direction)
            for p in range(1, len(snake)):
                if distance(snake[p-1], snake[p]) >= 2:
                    xy = get_move_xy(snake[p-1], snake[p])
                    snake[p] = translate(snake[p], *xy)

            positions.add((snake[-1].x, snake[-1].y))

    return len(positions)


print(move_snake(inputs, 2))
print(move_snake(inputs, 10))
