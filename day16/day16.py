import json
import re
from collections import deque
from functools import cache
from itertools import combinations, permutations

inputs = open("in")
test_inputs = open("in-test")


def parse_input(inputs):
    valves = {}
    for line in inputs:
        valve, rate, *tunnels = re.findall(r"[A-Z]{2}|\d+", line)
        if valve not in valves:
            valves[valve] = {"rate": int(rate), "tunnels": tunnels}
    return valves


valves = parse_input(test_inputs)


# def dfs(start, minutes):
#     paths = []

#     def _d(valve, minutes, path, opened, backtracks, steam=0):
#         path.append(valve)
#         paths.append((path.copy(), opened.copy(), steam))

#         if minutes <= 0:
#             return

#         if (rate := valves[valve]["rate"]) > 0 and valve not in opened:
#             print(path, steam)
#             minutes -= 1
#             steam += rate * minutes
#             opened.append(valve)

#         for tunnel in valves[valve]["tunnels"]:
#             if tunnel not in path:
#                 _d(tunnel, minutes-1, path, opened, backtracks, steam)
#             else:
#                 backtracks.append(tunnel)

#         for tunnel in backtracks:
#             _d(tunnel, minutes-1, path, opened, backtracks, steam)
    
#     _d(start, minutes, [], [], [])
#     return paths


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
        return start


start = Valve.from_valves(valves)






# steam = []
# for order_num, open_order in enumerate(permutations(flowing, len(flowing))):
#     steam.append([])
#     minutes = 30
#     valve = "AA"
#     # print(order_num, "======")
#     for next_valve in open_order:
#         if minutes <= 0:
#             break
#         # print("  ", valve, next_valve)
#         path = path_to(valve, next_valve)
#         time_taken = len(path) + 1
#         # print("  ", path, time_taken)
#         minutes -= time_taken
#         steam[order_num].append(valves[next_valve]["rate"] * minutes)
#         valve = next_valve

# print(max(dfs("AA", 30), key=lambda x: x[2]))


# print(max([sum(o) for o in steam]))
