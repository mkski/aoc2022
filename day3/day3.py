import string

with open("input") as f:
    inputs = f.read()

rucks = inputs.split("\n")

prio = {
    k: v
    for k, v in zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53))
}

s = 0
for ruck in rucks:
    n = len(ruck) // 2
    first, second = set(ruck[:n]), set(ruck[n:])
    common = list(first & second)[0]
    s += prio[common]

print(s)

size = 3
s = 0
for g in range(0, len(rucks), size):
    group = rucks[g:g+size]
    a, b, c = group
    common = list(set(a) & set(b) & set(c))[0]
    s += prio[common]

print(s)