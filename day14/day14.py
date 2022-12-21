inputs = open("in").read().split("\n")


class Point:

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"<Point {self.x},{self.y}>"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y


def make_line(p1, p2):
    startx, stopx = min(p1.x, p2.x), max(p1.x, p2.x)
    starty, stopy = min(p1.y, p2.y), max(p1.y, p2.y)

    if startx == stopx:
        return [Point(startx, y) for y in range(starty, stopy+1)]
    else:
        return [Point(x, starty) for x in range(startx, stopx+1)]


def get_rocks(inputs):
    rocks = set()
    maxy = 0
    for line in inputs:
        points = [Point(*p.split(",")) for p in line.split(" -> ")]

        for p in range(len(points)-1):
            maxy = max([maxy, points[p].y])
            rocks |= set(make_line(points[p], points[p+1]))
    return rocks, maxy


def move_sand(start, rocks, filled, floor):
    sand = start
    if sand.y >= floor:
        return None

    while sand not in rocks | filled and sand.y < floor:
        sand.y += 1

    sand.y -= 1
    left = Point(sand.x-1, sand.y+1)
    if left not in rocks | filled:
        return move_sand(left, rocks, filled, floor)

    right = Point(sand.x+1, sand.y+1)
    if right not in rocks | filled:
        return move_sand(right, rocks, filled, floor)

    return sand


def fill(rocks, floor):
    filled = set()
    while sand := move_sand(Point(500, 0), rocks, filled, floor):
        filled.add(sand)
        if sand == Point(500, 0):
            break
    return len(filled)


rocks, maxy = get_rocks(inputs)

print(fill(rocks, maxy))

floor = make_line(Point(-500, maxy+2), Point(1500, maxy+2))
rocks |= set(floor)
# this is horribly slow, need to fix
print(fill(rocks, maxy+2))
