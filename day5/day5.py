import re

inputs = open("in").read()
sections = inputs.split("\n\n")
crates, moves = sections


class Stack:

    def __init__(self):
        self.crates = []

    def add(self, crate):
        self.crates.append(crate)

    def push(self, crate):
        self.crates.insert(0, crate)

    def pop(self):
        return self.crates.pop(0)

    def push_multi(self, crates):
        self.crates = crates + self.crates

    def pop_n(self, n):
        popped, self.crates = self.crates[:n], self.crates[n:]
        return popped

    def peek(self):
        return self.crates[0]

    def __str__(self):
        return " ".join(self.crates)


def init_stacks(crates):
    stacks = [Stack() for _ in range(9)]
    for line in crates.split("\n")[:-1]:
        for i in range(1, len(line), 4):
            crate = line[i]
            if crate.isalpha():
                stacks[i//4].add(crate)
    return stacks


stacks = init_stacks(crates)
multi_stacks = init_stacks(crates)
for count, src, dest in re.findall(
    r"(?P<count>\d+) from (?P<src>\d+) to (?P<dest>\d+)",
    inputs
):
    count, src, dest = int(count), int(src), int(dest)
    for _ in range(count):
        stacks[dest-1].push(stacks[src-1].pop())
    multi_stacks[dest-1].push_multi(multi_stacks[src-1].pop_n(count))

print("".join([s.peek() for s in stacks]))
print("".join([s.peek() for s in multi_stacks]))