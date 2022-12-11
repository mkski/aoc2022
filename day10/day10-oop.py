import os

program = open("in").read().split("\n")


class Instruction:

    def __init__(self, cycles, eval_fn, *args):
        self.cycles = cycles
        self.eval_fn = eval_fn
        self.args = args

    def eval(self):
        self.eval_fn(*self.args)

    def __str__(self):
        return f"{self.eval_fn.__name__} {self.args}"


class Screen:

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.buffer = ""
        self.display = ["." * self.width] * self.height

    def swap(self):
        os.system("clear")
        self.display = self.buffer.split("\n")
        self.buffer = ""
        print("\n".join("".join(r) for r in self.display))

    def draw_frame(self, cycle, position):
        draw_pos = cycle % 40
        if draw_pos - 1 - position in (1, 0, -1):
            self.buffer += "#"
        else:
            self.buffer += "."

        if draw_pos == 0:
            self.buffer += "\n"

        if cycle % (self.width * self.height) == 0:
            self.swap()


class Cpu:

    def __init__(self, program):
        self.registers = {"X": 1}
        self.cycle = 1
        self.instructions = self.load_program(program)
        self.screen = Screen(40, 6)

    def load_program(self, program):
        instructions = []
        for line in program:
            match line.split():
                case ("noop",):
                    instructions.append(Instruction(0, self.noop))
                case "addx", val:
                    instructions.append(Instruction(1, self.addx, int(val)))
        return instructions

    def addx(self, value):
        self.registers["X"] += value

    def noop(self):
        pass

    def tick(self):
        self.cycle += 1
        self.draw()
        return self.cycle * self.registers["X"] if self.cycle % 40 == 20 else 0

    def run_instruction(self, instruction):
        total = 0
        for _ in range(instruction.cycles):
            total += self.tick()
        instruction.eval()
        total += self.tick()
        return total

    def draw(self):
        self.screen.draw_frame(self.cycle, self.registers["X"])

    def run(self):
        total = 0
        self.draw()
        for instruction in self.instructions:
            total += self.run_instruction(instruction)
        return total


cpu = Cpu(program)
print(cpu.run())
