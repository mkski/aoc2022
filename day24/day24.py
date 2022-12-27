from math import lcm
from collections import deque
import time

test_inputs = open("in-test2")
inputs = open("in")


class Blizzard:

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.vector = {
            ">": (0, 1),
            "v": (1, 0),
            "<": (0, -1),
            "^": (-1, 0)
        }[direction]

    def __hash__(self):
        return hash((self.x, self.y, self.direction))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction

    def __str__(self):
        return f"({self.x},{self.y}) {self.direction}"

    def move(self):
        self.x += self.vector[0]
        if self.x < 1:
            self.x = Blizzard.xmax
        elif self.x > Blizzard.xmax:
            self.x = 1

        self.y += self.vector[1]
        if self.y < 1:
            self.y = Blizzard.ymax
        elif self.y > Blizzard.ymax:
            self.y = 1

    @classmethod
    def from_inputs(cls, inputs):
        blizzards = set()
        xmax = ymax = 0
        for r, line in enumerate(inputs):
            ymax = len(line)
            xmax += 1
            for c, col in enumerate(line.strip()):
                if col not in ["#", "."]:
                    blizzards.add(cls(r, c, col))
        
        cls.xmax = xmax - 2
        cls.ymax = ymax - 2
        return blizzards, cls.xmax, cls.ymax


def get_grid(blizzards, xmax, ymax, show=True):
    grid = [["#"]*(ymax+2)]
    for r in range(xmax):
        grid.append(["#"])
        for c in range(ymax):
            grid[r+1].append(".")
        grid[r+1].append("#")
    grid.append(["#"]*(ymax+2))

    grid[0][1] = "."
    grid[-1][-2] = "."

    positions = {}
    for b in blizzards:
        pos = (b.x, b.y)
        if pos in positions:
            positions[pos].append(b)
        else:
            positions[pos] = [b]

    for p, b in positions.items():
        if len(b) > 1:
            grid[p[0]][p[1]] = str(len(b))
        else:
            grid[p[0]][p[1]] = b[0].direction

    if show:
        for r in grid:
            print("".join(r))
    
    return grid


def build_grid_with_time():
    blizzards, xmax, ymax = Blizzard.from_inputs(inputs)
    cycle = lcm(xmax, ymax)

    grid_minutes = [get_grid(blizzards, xmax, ymax, show=False)]
    for _ in range(cycle):
        for b in blizzards:
            b.move()
        grid_minutes.append(get_grid(blizzards, xmax, ymax, show=False))

    return grid_minutes, xmax, ymax, cycle


def print_grid(grid, minute):
    for r in grid[minute]:
        print("".join(r))


def bfs(grid, start, stop, xmax, ymax, cycle, minutes=None):
    # queue the start position - (minute, row, col) = (0, 0, 1)
    queue = deque([(minutes or 0, start[0], start[1])])
    checked = set()

    while queue:
        pos = queue.popleft()
        minute, x, y = pos

        neighbors = [
            (minute+1, x+1, y),  # spend one minute moving down
            (minute+1, x, y+1),  # spend one minute moving right
            (minute+1, x, y-1),  # spend one minute moving left
            (minute+1, x-1, y),  # spend one minute moving up
            (minute+1, x, y)     # spend one minute standing still
        ]

        for nm, nx, ny in neighbors:
            # if the neighbor is the goal, add the current time spent for consideration
            if (nx, ny) == (stop[0], stop[1]):
            # if (nx, ny) == (5, 100):
                return nm

            # check if the neighbor is out of bounds
            if (nx < 1 or ny < 1 or nx > xmax or ny > ymax) and not (nx, ny) in (start, stop):
                continue

            if (nm, nx, ny) in checked:
                continue
            
            # queue the neighbor if it's not occupied by a blizzard
            if grid[nm%cycle][nx][ny] == ".":
                queue.append((nm, nx, ny))
            
            checked.add((nm, nx, ny))


s = time.time()
grid, xmax, ymax, cycle = build_grid_with_time()
print(f"precompute {time.time()-s:0.02f}s\n")

s = time.time()
start = (0, 1)
stop = (xmax+1, ymax)
there = bfs(grid, start, stop, xmax, ymax, cycle)
print(f"part 1: {there}")
print(f"{time.time()-s:0.02f}s\n")

s = time.time()
start, stop = stop, start
back = bfs(grid, start, stop, xmax, ymax, cycle, minutes=there)

start, stop = stop, start
there_again = bfs(grid, start, stop, xmax, ymax, cycle, minutes=back)
print(f"part 2: {there_again}")
print(f"{time.time()-s:0.02f}s")
