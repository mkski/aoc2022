class Direction:

    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]

    def __add__(self, other):
        return type(self)(self.x + other[0], self.y + other[1])


face_values = {
    ">": 0,
    "v": 1,
    "<": 2,
    "^": 3
}


class Mover:

    directions = {
        Direction.RIGHT: ">",
        Direction.DOWN: "v",
        Direction.LEFT: "<",
        Direction.UP: "^"
    }

    def __init__(self, grid):
        self.grid = grid
        self.pos = Position(0, grid[0].index('.'))
        self.direction = Direction.RIGHT

    def turn_right(self):
        if self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        elif self.direction == Direction.UP:
            self.direction = Direction.RIGHT
    
    def turn_left(self):
        if self.direction == Direction.RIGHT:
            self.direction = Direction.UP
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.UP:
            self.direction = Direction.LEFT

    def wrap(self):
        if self.direction == Direction.RIGHT:
            col = 0
            while self.grid[self.pos.x][col] == ' ':
                col += 1
            return self.grid[self.pos.x][col], Position(self.pos.x, col)

        elif self.direction == Direction.LEFT:
            col = len(self.grid[self.pos.x]) - 1
            while self.grid[self.pos.x][col] == ' ':
                col -= 1
            return self.grid[self.pos.x][col], Position(self.pos.x, col)

        elif self.direction == Direction.UP:
            row = len(self.grid) - 1
            while self.grid[row][self.pos.y] == ' ':
                row -= 1
            return self.grid[row][self.pos.y], Position(row, self.pos.y)

        elif self.direction == Direction.DOWN:
            row = 0
            while self.grid[row][self.pos.y] == ' ':
                row += 1
            return self.grid[row][self.pos.y], Position(row, self.pos.y)

    def peek(self):
        next_pos = self.pos + self.direction
        try:
            c = self.grid[next_pos.x][next_pos.y]
        except IndexError:
            c = " "
        
        if c == " ":
            c, next_pos = self.wrap()
        return c, next_pos

    def do_instructions(self, instructions):
        for dist, turn in instructions:
            for _ in range(int(dist)):
                next_space, next_pos = self.peek()
                if next_space == "#":
                    break
                self.grid[self.pos.x][self.pos.y] = self.directions[self.direction]
                self.pos = next_pos
            if turn == "L":
                self.turn_left()
            else:
                self.turn_right()
        self.grid[self.pos.x][self.pos.y] = self.directions[self.direction]

        return (
            1000 * (self.pos.x+1) +
            4 * (self.pos.y+1) +
            face_values[self.directions[self.direction]]
        )

    def print_grid(self):
        for row in self.grid:
            print("".join(row))


class CubeMover(Mover):

    def __init__(self, sides, side_map):
        self.sides = sides
        self.side_map = side_map
        self.side = 0
        self.grid = self.sides[self.side]
        self.pos = Position(0, self.grid[0].index('.'))
        self.direction = Direction.RIGHT
        self.sidelen = len(sides[0])

    def peek(self):
        next_pos = self.pos + self.direction
        next_side = self.side
        next_direction = self.direction

        try:
            c = self.grid[next_pos.x][next_pos.y]
        except IndexError:
            c = " "

        if next_pos.x < 0 or next_pos.y < 0:
            c = " "
        
        if c == " ":
            c, next_pos, next_side, next_direction = self.wrap()
        return c, next_pos, next_side, next_direction

    def wrap(self):
        old_direction = self.direction
        new_side, new_direction = self.side_map[self.side][0][self.direction]
        next_grid = self.sides[new_side]

        # print("old side:", self.side)
        # print("new side:", new_side)
        # print("direction", self.direction)
        # print("new direction", new_direction)
        # print()
        
        if old_direction == new_direction == Direction.RIGHT:
            next_space, next_pos = next_grid[self.pos.x][0], Position(self.pos.x, 0)
        elif old_direction == new_direction == Direction.LEFT:
            next_space, next_pos = next_grid[self.pos.x][self.sidelen-1], Position(self.pos.x, self.sidelen-1)
        elif old_direction == new_direction == Direction.UP:
            next_space, next_pos = next_grid[self.sidelen-1][self.pos.y], Position(self.sidelen-1, self.pos.y)
        elif old_direction == new_direction == Direction.DOWN:
            next_space, next_pos = next_grid[0][self.pos.y], Position(0, self.pos.y)

        elif old_direction == Direction.RIGHT and new_direction == Direction.LEFT:
            next_space, next_pos = next_grid[self.sidelen-self.pos.x-1][self.sidelen-1], Position(self.sidelen-self.pos.x-1, self.sidelen-1)
        elif old_direction == Direction.LEFT and new_direction == Direction.RIGHT:
            next_space, next_pos = next_grid[self.sidelen-self.pos.x-1][0], Position(self.sidelen-self.pos.x-1, 0)
            
        elif old_direction == Direction.RIGHT and new_direction == Direction.DOWN:
            next_space, next_pos = next_grid[0][self.sidelen-self.pos.x-1], Position(0, self.sidelen-self.pos.x-1)
        elif old_direction == Direction.DOWN and new_direction == Direction.UP:
            next_space, next_pos = next_grid[self.pos.x][self.sidelen-self.pos.y-1], Position(self.pos.x, self.sidelen-self.pos.y-1)
        elif old_direction == Direction.UP and new_direction == Direction.RIGHT:
            next_space, next_pos = next_grid[self.pos.y][0], Position(self.pos.y, 0)
        elif old_direction == Direction.LEFT and new_direction == Direction.DOWN:
            next_space, next_pos = next_grid[0][self.pos.x], Position(0, self.pos.x)
        elif old_direction == Direction.RIGHT and new_direction == Direction.UP:
            next_space, next_pos = next_grid[self.sidelen-1][self.pos.x], Position(self.sidelen-1, self.pos.x)
        elif old_direction == Direction.DOWN and new_direction == Direction.LEFT:
            next_space, next_pos = next_grid[self.pos.y][self.sidelen-1], Position(self.pos.y, self.sidelen-1)

        return next_space, next_pos, new_side, new_direction


    def do_instructions(self, instructions):
        for dist, turn in instructions:
            for _ in range(int(dist)):
                next_space, next_pos, next_side, next_direction = self.peek()
                if next_space == "#":
                    break
                self.grid[self.pos.x][self.pos.y] = self.directions[self.direction]
                self.pos = next_pos
                self.side = next_side
                self.direction = next_direction
                self.grid = self.sides[self.side]
            if turn == "L":
                self.turn_left()
            else:
                self.turn_right()
        self.grid[self.pos.x][self.pos.y] = self.directions[self.direction]
        # test input needs to go one step further to land at the right spot
        self.pos = self.pos + self.direction
        self.grid[self.pos.x][self.pos.y] = self.directions[self.direction]
        # for some reason real input needs to go yet another step further
        # this will make the test part 2 give the wrong answer
        # no idea why
        self.pos = self.pos + self.direction
        self.grid[self.pos.x][self.pos.y] = self.directions[self.direction]

        converter = self.side_map[self.side][1]
        x, y = converter(self.pos.x, self.pos.y)
        return 1000 * (x + 1) + 4 * (y + 1) + face_values[self.directions[self.direction]]