import re
from copy import deepcopy

from mover import Mover, Direction, CubeMover

inputs = open("in").read()
test_inputs = open("in-test").read()


def parse_input(inputs):
    grid, instructions = inputs.split("\n\n")
    m = []
    lines = [line for line in grid.split("\n")]
    maxlen = max(len(line) for line in lines)

    for line in lines:
        row = []
        for c in line:
            row.append(c)
        
        if len(line) < maxlen:
            for _ in range(maxlen - len(line)):
                row.append(" ")
        m.append(row)
    
    return m, instructions

print("tests:")
test_m, test_inst = parse_input(test_inputs)
test_inst = re.findall(r"(\d+)(L|R)", test_inst)
test_mover = Mover(deepcopy(test_m))
print(test_mover.do_instructions(test_inst))

test_sides = [
    [[c for c in r[8:12]] for r in test_m[:4]],      # side 1
    [[c for c in r[0:4]] for r in test_m[4:8]],      # side 2
    [[c for c in r[4:8]] for r in test_m[4:8]],      # side 3
    [[c for c in r[8:12]] for r in test_m[4:8]],      # side 4
    [[c for c in r[8:12]] for r in test_m[8:12]],      # side 5
    [[c for c in r[12:16]] for r in test_m[8:12]],      # side 6
]

test_side_map = {
    0: (
        {
            Direction.LEFT: (2, Direction.DOWN),
            Direction.RIGHT: (5, Direction.LEFT),
            Direction.UP: (1, Direction.DOWN),
            Direction.DOWN: (3, Direction.DOWN)
        },
        lambda x, y: (x, y + 8)
    ),
    1: (
        {
            Direction.LEFT: (5, Direction.UP),
            Direction.RIGHT: (2, Direction.RIGHT),
            Direction.UP: (0, Direction.DOWN),
            Direction.DOWN: (4, Direction.UP)
        },
        lambda x, y,: (x + 4, y)
    ),
    2: (
        {
            Direction.LEFT: (1, Direction.LEFT),
            Direction.RIGHT: (3, Direction.RIGHT),
            Direction.UP: (0, Direction.RIGHT),
            Direction.DOWN: (4, Direction.RIGHT)
        },
        lambda x, y,: (x + 4, y + 4)
    ),
    3: (
        {
            Direction.LEFT: (2, Direction.LEFT),
            Direction.RIGHT: (5, Direction.DOWN),
            Direction.UP: (0, Direction.UP),
            Direction.DOWN: (4, Direction.DOWN)
        },
        lambda x, y,: (x + 4, y + 8)
    ),
    4: (
            {
            Direction.LEFT: (2, Direction.UP),
            Direction.RIGHT: (5, Direction.RIGHT),
            Direction.UP: (3, Direction.UP),
            Direction.DOWN: (1, Direction.UP)
        },
        lambda x, y,: (x + 8, y + 8)
    ),
    5: (
            {
            Direction.LEFT: (4, Direction.LEFT),
            Direction.RIGHT: (0, Direction.LEFT),
            Direction.UP: (3, Direction.LEFT),
            Direction.DOWN: (1, Direction.RIGHT)
        },
        lambda x, y,: (x + 8, y + 12)
    )
}

test_cube_mover = CubeMover(test_sides, test_side_map)
print(test_cube_mover.do_instructions(test_inst))
print()


print("real:")
m, instructions = parse_input(inputs)
instructions = re.findall(r"(\d+)(L|R)", instructions)
mover = Mover(deepcopy(m))
print(mover.do_instructions(instructions))

# cube from input:
#        ___________ 
#       |     |     |   row 0
#       |  1  |  2  |    
#       |_____|_____|
#       |     |  row 50
#       |  3  |   
#  _____|_____|
# |     |     |  row 100
# |  5  |  4  |    
# |_____|_____|
# |     |   row 150
# |  6  |  
# |_____|

sides = [
    [[c for c in r[50:100]] for r in m[:50]],      # side 1
    [[c for c in r[100:150]] for r in m[:50]],     # side 2
    [[c for c in r[50:100]] for r in m[50:100]],   # side 3
    [[c for c in r[50:100]] for r in m[100:150]],  # side 4
    [[c for c in r[:50]] for r in m[100:150]],     # side 5
    [[c for c in r[:50]] for r in m[150:200]],     # side 5
]

side_map = {
    0: (
        {
            Direction.LEFT: (4, Direction.RIGHT),
            Direction.RIGHT: (1, Direction.RIGHT),
            Direction.UP: (5, Direction.RIGHT),
            Direction.DOWN: (2, Direction.DOWN)
        },
        lambda x, y: (x, y + 50)
    ),
    1: (
        {
            Direction.LEFT: (0, Direction.LEFT),
            Direction.RIGHT: (3, Direction.LEFT),
            Direction.UP: (5, Direction.UP),
            Direction.DOWN: (2, Direction.LEFT)
        },
        lambda x, y,: (x, y + 100)
    ),
    2: (
        {
            Direction.LEFT: (4, Direction.DOWN),
            Direction.RIGHT: (1, Direction.UP),
            Direction.UP: (0, Direction.UP),
            Direction.DOWN: (3, Direction.DOWN)
        },
        lambda x, y,: (x + 50, y + 50)
    ),
    3: (
        {
            Direction.LEFT: (4, Direction.LEFT),
            Direction.RIGHT: (1, Direction.LEFT),
            Direction.UP: (2, Direction.UP),
            Direction.DOWN: (5, Direction.LEFT)
        },
        lambda x, y,: (x + 100, y + 50)
    ),
    4: (
            {
            Direction.LEFT: (0, Direction.RIGHT),
            Direction.RIGHT: (3, Direction.RIGHT),
            Direction.UP: (2, Direction.RIGHT),
            Direction.DOWN: (5, Direction.DOWN)
        },
        lambda x, y,: (x + 100, y)
    ),
    5: (
            {
            Direction.LEFT: (0, Direction.DOWN),
            Direction.RIGHT: (3, Direction.UP),
            Direction.UP: (4, Direction.UP),
            Direction.DOWN: (1, Direction.DOWN)
        },
        lambda x, y,: (x + 150, y)
    )
}

cube_mover = CubeMover(sides, side_map)
print(cube_mover.do_instructions(instructions))
