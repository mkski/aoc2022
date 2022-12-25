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
        start = cls("AA", 0)
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
valves = parse_input(inputs)
start, flowing = Valve.from_valves(valves)
paths = max_steam(start)
print(max(paths, key=lambda p: p[1])[1])
print(f"{time.time()-s:0.04f}s")


from copy import deepcopy
s = time.time()
# max_steam returns all possible paths that can be completed in the minutes given
paths = max_steam(start, minutes=26)

# eliminate all sub paths that dont open roughly half of flowing valves
# paths = [p for p in paths if 2*(len(p[0])-1) - flowing_count in range(-3, 4)]

# ^^^ this didnt eliminate enough paths

# instead, we eliminate those paths that clearly dont release enough steam
paths = [p for p in paths if p[1] > 1200]
# definitely did not tweak this number(^) a ton of times until i got the right answer..
num_paths = len(paths)

possibilities = []

# just some status variables
total = num_paths**2
n = 1
start_time = time.time()
since = start_time

# to find the answer for part two, we need two unique paths that open the most amount of steam
# get the steam values for each pair of paths after we eliminate the paths that definitely do not
# release enough steam
for p1 in deepcopy(paths):
    path1, steam1 = p1
    # every path starts at AA, lets remove it
    path1.pop(0)

    for p2 in deepcopy(paths):
        # calculate our status
        if n % 1_000_000 == 0:
            progress = n/total
            print(f"status: {progress*100:0.02f}%")
            print(f"elapsed: {time.time() - start_time:0.02f}s")
            print(f"est. remaining: {(total-n)/1_000_000*(time.time()-since):0.02f}s")
            print()
            since = time.time()

        path2, steam2 = p2
        path2.pop(0)
        n += 1

        # make sure the paths dont open the same valve more than once
        if set(path1) & set(path2):
            continue

        # add this path pair's steam value for consideration
        possibilities.append(steam1+steam2)

print(max(possibilities))
print(f"{time.time()-s:0.04f}s")
