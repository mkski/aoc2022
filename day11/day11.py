import operator
import re
from functools import reduce

inputs = open("in").read().split("\n\n")

items_re = re.compile(r"Starting items: (?P<g>[^\n]+)")
ops_re = re.compile(r"Operation: (?P<g>[^\n]+)")
test_re = re.compile(r"Test: (?P<g>[^\n]+)")
true_re = re.compile(r"If true: (?P<g>[^\n]+)")
false_re = re.compile(r"If false: (?P<g>[^\n]+)")


operations = {
    "+": operator.add,
    # "-": operator.sub,
    "*": operator.mul,
    # "/": operator.floordiv
}


class Monkey:

    def __init__(self, id, config):
        self.id = id
        self.items = list(map(int, re.search(items_re, config).group("g").split(", ")))
        self.op = re.search(ops_re, config).group("g")
        self.test = re.search(test_re, config).group("g")
        self.true = re.search(true_re, config).group("g")
        self.false = re.search(false_re, config).group("g")

        self.true_monkey = int(self.true.split()[-1])
        self.false_monkey = int(self.false.split()[-1])
        self.test_value = int(self.test.split()[-1])

        self.inspected = 0

    def __str__(self):
        return f"<Monkey {self.id}>"

    def test_item(self, item):
        return item % int(self.test_value) == 0

    def inspect(self, monkeys, reduce_worry=True):
        try:
            item = self.items.pop()
        except IndexError:
            return None

        op, tar = self.op.split()[-2:]
        if tar == "old":
            target = item
        else:
            target = int(tar)

        item = operations[op](item, target)
        self.inspected += 1
        if reduce_worry:
            item = item // 3
        else:
            item = item % reduce(operator.mul, [m.test_value for m in monkeys])

        if self.test_item(item):
            self.throw_to(item, monkeys[self.true_monkey])
        else:
            self.throw_to(item, monkeys[self.false_monkey])

        return item

    def throw_to(self, item, monkey):
        monkey.items.append(item)

    def do_round(self, monkeys):
        self.inspected += len(self.items)
        for item in self.items:
            self.throw_to(
                item,
                monkeys[self.true_monkey]
                if self.test_item(item) else
                monkeys[self.false_monkey])


def do_rounds(count, reduce_worry=True):
    for r in range(count):
        for m in monkeys:
            inspected = m.inspect(monkeys, reduce_worry=reduce_worry)
            while inspected is not None:
                inspected = m.inspect(monkeys, reduce_worry=reduce_worry)


def make_monkeys(i):
    monkeys = []
    for n, monkey in enumerate(i):
        monkeys.append(Monkey(n, monkey))
    return monkeys


monkeys = make_monkeys(inputs)
do_rounds(20)
print(operator.mul(*sorted([m.inspected for m in monkeys])[-2:]))

monkeys = make_monkeys(inputs)
do_rounds(10_000, reduce_worry=False)
print(operator.mul(*sorted([m.inspected for m in monkeys])[-2:]))