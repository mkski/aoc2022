program = open("in").read().split()

adds = [1] + [0 if t in ("addx", "noop") else int(t) for t in program]
total = 0
output = ""
for cycle, _ in enumerate(adds[:-1], 1):
    x_register = sum(adds[:cycle])
    position = cycle % 40

    total += cycle * x_register if position == 20 else 0
    output += "#" if position - 1 - x_register in (1, 0, -1) else '.'

    if position == 0:
        output += "\n"

print(total)
print(output)
