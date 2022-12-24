import time
import re
from collections import deque
from functools import cache
from itertools import product

inputs = open("in")
test_inputs = open("in-test")


def parse_input(inputs):
    valves = {}
    for line in inputs:
        valve, rate, *tunnels = re.findall(r"[A-Z]{2}|\d+", line)
        if valve not in valves:
            valves[valve] = {"rate": int(rate), "tunnels": tunnels}
    return valves



@cache
def path_to(s, e):
    queue = deque([(s, [])])
    visited = set([s])
    if s == e:
        return []

    while queue:
        valve, path = queue.popleft()
        if valve == e:
            return path

        for tunnel in valves[valve]["tunnels"]:
            if tunnel not in visited:
                visited.add(tunnel)
                queue.append((tunnel, path + [tunnel]))
    return None


class Tunnel:
    
    def __init__(self, from_valve, to_valve, weight):
        self.from_valve = from_valve
        self.to_valve = to_valve
        self.weight = weight

class Valve:

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.tunnels = []

    def add_tunnel(self, tunnel):
        self.tunnels.append(tunnel)

    @classmethod
    def from_valves(cls, valves):
        flowing = [cls(name, v["rate"]) for name, v in valves.items() if v["rate"] > 0]
        start = Valve("AA", 0)
        for valve in flowing:
            path_len = len(path_to(start.name, valve.name))
            start.add_tunnel(Tunnel(start, valve, path_len))
            for valve2 in flowing:
                if not valve.name ==valve2.name:
                    path_len = len(path_to(valve.name, valve2.name))
                    valve.add_tunnel(Tunnel(valve, valve2, path_len))
        return start, flowing


def max_steam(start, minutes=30):
    minutes += 1

    def _d(valve, minutes, path, paths, opened, steam=0):
        this_path = path.copy()
        this_path.append(valve.name)
        
        if valve.name not in opened:
            minutes -= 1
            steam += valve.rate * minutes

        paths.append((this_path, steam))

        for tunnel in valve.tunnels:
            if tunnel.to_valve.name not in path and tunnel.weight < minutes-1:
                _d(tunnel.to_valve, minutes-tunnel.weight, this_path, paths, opened, steam)

        return paths

    return _d(start, minutes, [], [], [])


s = time.time()
valves = parse_input(test_inputs)
start, flowing = Valve.from_valves(valves)
paths = max_steam(start)
print(max(paths, key=lambda p: p[1])[1])
print(f"{time.time()-s:0.04f}s")


from copy import deepcopy
paths = max_steam(start, minutes=26)

# for p in paths:
#     if p[0] == ["AA", "DD", "HH", "EE"]:
#         print(p[1])
#     if p[0] == ["AA", "JJ", "BB", "CC"]:
#         print(p[1])

flowing_set = set([v.name for v in flowing])
possibilities = {}
for p1, p2 in product(paths, deepcopy(paths)):
    p1, s1 = p1
    p2, s2 = p2
    if not p1 or not p2 or 1 in [len(p1), len(p2)]:
        continue

    p1.pop(0)
    p2.pop(0)
    v = frozenset(set(p1) | set(p2))
    if v in possibilities and v == frozenset(flowing_set):
        possibilities[v] = max(s1+s2, possibilities[v])
    else:
        possibilities[v] = s1+s2
print(possibilities)


# s = time.time()
# print(max_steam(start, minutes=26))
# print(f"{time.time()-s:0.04f}s")
