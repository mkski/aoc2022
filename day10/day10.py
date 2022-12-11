program = open("input").read().split()


def get_adds(p):
    yield 1
    for token in p:
        yield 0 if token in ("addx", "noop") else int(token)


adds = list(get_adds(program))
total = 0
output = ""
for cycle, _ in enumerate(adds[:-1], 1):
    x_register = sum(adds[:cycle])
    position = cycle % 40

    if position == 20:
        total += cycle * x_register

    if position - 1 - x_register in (1, 0, -1):
        output += "#"
    else:
        output += "."

    if position == 0:
        output += "\n"

print(total)
print(output)
