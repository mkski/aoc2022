import operator
import time

from sympy import Eq, solve, symbols

test_inputs = open("in-test")
inputs = open("in")

operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}


class Monkey:

    def __init__(self, name, value=None, op=None, left=None, right=None):
        self.name = name
        self._value = value
        self.op = op
        self.left = left
        self.right = right

    @property
    def value(self):
        if self._value is None:
            return int(operations[self.op](self.left.value, self.right.value))
        else:
            return int(self._value)

    def __str__(self):
        if self._value is None:
            return (
                f"<Monkey {self.name=} {str(self.left)} "
                f"{self.op=} {str(self.right)}>"
            )
        else:
            return f"<Monkey {self.name=} {self._value}>"


def parse_input(inputs):
    monkeys = {}
    for line in inputs:
        match line.split():
            case str() as name, str() as leftn, str() as op, str() as rightn:
                name = name.strip(":")

                left = monkeys.get(leftn, Monkey(leftn))
                monkeys[leftn] = left
                right = monkeys.get(rightn, Monkey(rightn))
                monkeys[rightn] = right

                if name not in monkeys:
                    monkeys[name] = Monkey(name, op=op, left=left, right=right)
                else:
                    monkeys[name].left = left
                    monkeys[name].right = right
                    monkeys[name].op = op

            case str() as name, str() as value:
                name = name.strip(":")
                if name not in monkeys:
                    monkeys[name] = Monkey(name, value=value)
                else:
                    monkeys[name]._value = value
    return monkeys


def search_humn(monkey):
    if monkey.name == "humn":
        return True
    elif monkey.left is None and monkey.right is None:
        return False
    return search_humn(monkey.left) or search_humn(monkey.right)


def find_value(monkey):
    # find where humn is in the tree, left or right sub-tree
    is_left = search_humn(monkey.left)
    # find the value the humn side (left or right) needs to equal
    to_match = monkey.right.value if is_left else monkey.left.value
    return is_left, to_match


def get_humn_value(monkey, is_left, to_match):

    def build_exp(m):
        # builds the expression that needs to equal `to_match`
        if m.name == "humn":
            return symbols("x")
        elif m.left is None and m.right is None:
            return m.value
        return operations[m.op](build_exp(m.left), build_exp(m.right))

    return int(
        solve(
            Eq(
                build_exp(monkey.left) if is_left else build_exp(monkey.right),
                to_match
            )
        )[0]
    )


start = time.time()
monkeys = parse_input(inputs)
root = monkeys["root"]
print(root.value)
print(f"{time.time() - start:0.4f}s")
print()

start = time.time()
is_left, to_match = find_value(root)
print(get_humn_value(root, is_left, to_match))
print(f"{time.time() - start:0.4f}s")
