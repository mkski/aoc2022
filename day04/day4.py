inputs = open("in").read().split("\n")

c = 0
s = 0
for pair in inputs:
    first, second = pair.split(",")
    fstart, fend = first.split("-")
    sstart, send = second.split("-")

    first = set(range(int(fstart), int(fend)+1))
    second = set(range(int(sstart), int(send)+1))

    l = len(first & second)
    if l in (len(first), len(second)):
        c += 1
    if len(first & second) > 0:
        s += 1
print(c)
print(s)
