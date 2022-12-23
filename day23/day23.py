import os

inputs = open("in")


class Position:
    def __init__(self, r, c):
        self.r = r
        self.c = c
    def __str__(self):
        return f"({self.r}, {self.c})"
    def __hash__(self):
        return hash((self.r, self.c))
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c


def parse_input(inputs):
    positions = []
    for r, line in enumerate(inputs):
        for c, col in enumerate(line):
            if col == "#":
                positions.append(Position(r, c))
    return positions


def propose_n(pos, positions):
    return (
        Position(pos.r-1, pos.c) 
        if all(p not in positions for p in set((Position(pos.r-1, c) for c in range(pos.c-1, pos.c+2)))) else
        None
    )

def propose_s(pos, positions):
    return (
        Position(pos.r+1, pos.c)
        if all(p not in positions for p in set((Position(pos.r+1, c) for c in range(pos.c-1, pos.c+2)))) else
        None
    )

def propose_e(pos, positions):
    return (
        Position(pos.r, pos.c+1)
        if all(p not in positions for p in set((Position(r, pos.c+1) for r in range(pos.r-1, pos.r+2)))) else
        None
    )

def propose_w(pos, positions):
    return (
        Position(pos.r, pos.c-1)
        if all(p not in positions for p in set((Position(r, pos.c-1) for r in range(pos.r-1, pos.r+2)))) else
        None
    )


propose_order = [propose_n, propose_s, propose_w, propose_e]


def has_space(pos, positions):
    return all(
        p not in positions
        for p in
        set([Position(pos.r-1, c) for c in range(pos.c-1, pos.c+2)] +
        [Position(pos.r+1, c) for c in range(pos.c-1, pos.c+2)] +
        [Position(pos.r, pos.c-1), Position(pos.r, pos.c+1)])
    )


def min_max(positions):
    rmin = cmin = 9999
    rmax = cmax = 0
    for p in positions:
        rmin, cmin = min(rmin, p.r), min(cmin, p.c)
        rmax, cmax = max(rmax, p.r), max(cmax, p.c)
    return rmin, rmax, cmin, cmax


def get_empty(positions):
    rmin, rmax, cmin, cmax = min_max(positions)
    return (rmax-rmin+1) * (cmax-cmin+1) - len(positions)


def print_state(positions):
    rmin, rmax, cmin, cmax = min_max(positions)
    rows = rmax-rmin+1
    cols = cmax-cmin+1

    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            grid[r].append('.')
    
    for p in positions:
        grid[p.r-rmin][p.c-cmin] = "#"
    
    for row in grid:
        print("".join(row))
            

positions = parse_input(inputs)

def do_rounds(positions, count=None):
    turn = 1
    while True:
        elves_to_move = set()
        for p in positions:
            if not has_space(p, set(positions)):
                elves_to_move.add(p)
        if len(elves_to_move) == 0:
            return turn
        # print(turn, len(elves_to_move))
        
        propositions = {}
        for e in elves_to_move:
            for propose in propose_order:
                if new_pos := propose(e, set(positions)):
                    if new_pos not in propositions:
                        propositions[new_pos] = [e]
                    else:
                        propositions[new_pos].append(e)
                    break
        
        for p, elves in propositions.items():
            if len(elves) > 1:
                continue
            elves[0].r = p.r
            elves[0].c = p.c
        
        propose_order.append(propose_order.pop(0))
        turn += 1
        if count and turn > count:
            return turn

# do_rounds(positions, count=10)
# print(get_empty(positions))
print(do_rounds(positions))
