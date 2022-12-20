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


def dfs(start, minutes):
    pass


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


flowing = [name for name, v in valves.items() if v["rate"] > 0]


steam = []
for order_num, open_order in enumerate(permutations(flowing, len(flowing))):
    print(order_num)
    steam.append([])
    minutes = 30
    valve = "AA"
    # print(order_num, "======")
    for next_valve in open_order:
        if minutes <= 0:
            break
        # print("  ", valve, next_valve)
        path = path_to(valve, next_valve)
        time_taken = len(path) + 1
        # print("  ", path, time_taken)
        minutes -= time_taken
        steam[order_num].append(valves[next_valve]["rate"] * minutes)
        valve = next_valve


print(max([sum(o) for o in steam]))
# print(paths_from_valve(valves, "AA"))
# print(open_valves_dynamic(valves, "AA"))
