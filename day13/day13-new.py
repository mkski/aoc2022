from ast import literal_eval
from itertools import zip_longest
from functools import cmp_to_key

pairs = open("in").read().split("\n\n")


def compare(left, right):
    if left is None:
        return -1
    elif right is None:
        return 1

    match left, right:
        case list(), list():
            for left, right in zip_longest(left, right):
                order = compare(left, right)
                if order == 0:
                    continue
                return order
            return 0

        case int(), int():
            return left - right
        case int(), list():
            return compare([left], right)
        case list(), int():
            return compare(left, [right])

packets = []
s = 0
for n, pair in enumerate(pairs, 1):
    left, right = [literal_eval(p) for p in pair.split("\n")]
    packets.extend([[left], [right]])
    order = compare(left, right) < 0
    s += n if order else 0
print(s)

packets.extend([[[6]], [[2]]])

ordered = sorted(packets, key=cmp_to_key(compare))
print((ordered.index([[2]])+1) * (ordered.index([[6]])+1))
