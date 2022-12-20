import re
import time
from itertools import product

inputs = open("in").read().split("\n")
test_inputs = open("in-test").read().split("\n")


def dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def parse_inputs(inputs):
    xmin = 99999999
    xmax = 0
    dmax = 0
    sensors = {}
    distances = {}
    for line in inputs:
        s = re.search(r"^Sensor at x=-?(?P<sx>\d+), y=-?(?P<sy>\d+):", line)
        sensor = int(s.group(1)), int(s.group(2))

        b = re.search(r"closest beacon is at x=-?(?P<bx>\d+), y=-?(?P<by>\d+)$", line)
        beacon = int(b.group(1)), int(b.group(2))

        sensors[sensor] = beacon
        distances[sensor] = dist(sensor, beacon)
        xmin = min([xmin, sensor[0], beacon[0]])
        xmax = max([xmax, sensor[0], beacon[0]])
        dmax = max([dmax, distances[sensor]])
    return sensors, distances, xmin, xmax, dmax


def parse_numbers(inputs):
    sensors = []
    for line in inputs:
        sensors.append(tuple(map(int, re.findall(r"-?\d+", line))))
    return sensors


def scan_y(inputs, y):
    sensors, distances, xmin, xmax, dmax = parse_inputs(inputs)
    s = 0
    for x in range(xmin-dmax-1, xmax+dmax+1):
        point = (x, y)
        if point in sensors.keys() or point in sensors.values():
            continue

        for sensor in distances:
            if dist((x, y), sensor) <= distances[sensor]:
                s += 1
                break
    return s


def find_beacon(inputs, maxv):
    sensor_values = parse_numbers(inputs)
    radii = {
        (sx, sy): dist((sx, sy), (bx, by))
        for sx, sy, bx, by in sensor_values
    }

    for s1, s2 in product(radii.keys(), radii.keys()):
        # for each pair of sensors (s1 and s2), get the 4 lines representing
        # each sensor's boundary
        s1x, s1y = s1
        s2x, s2y = s2
        r1, r2 = radii[s1], radii[s2]
        # boundary lines have the equations (in slope-intercept form)
        #   y = x + r
        #   y = x - r
        #   y = -x + r
        #   y = -x - r
        # converting to general form (Ax + By + C = 0):
        #   y = x + r
        #   y - r = x
        #   -x + y - r = 0
        # multiply both sides by -1
        #   x - y + r = 0

        # we also add 1 since we want the line representing just outside a sensor's boundary
        s1_pos_bounds = [
            #   y = x + r  (subtract x and r from both sides)
            #   -x + y - r = 0  (multiply both sides by -1)
            #   x - y + r = 0
            (s1x - s1y + r1 + 1),
            #   y = x - r  (add r and subtract x from both sides)
            #   -x + y + r = 0  (multiply both sides by -1)
            #   x - y - r = 0
            (s1x - s1y - r1 + 1)
        ]
        s1_neg_bounds = [
            # y = -x - r  (add x and r to both sides)
            # y + x + r = 0
            (s1x + s1y + r1 + 1),
            # y = -x + r  (add x and subtract r from both sides)
            # y + x - r = 0
            (s1x + s1y - r1 + 1)
        ]
        # do the same for the other sensor
        s2_pos_bounds = [
            #   y = x + r  (subtract x and r from both sides)
            #   -x + y - r = 0  (multiply both sides by -1)
            #   x - y + r = 0
            (s2x - s2y + r2 + 1),
            #   y = x - r  (add r and subtract x from both sides)
            #   -x + y + r = 0  (multiply both sides by -1)
            #   x - y - r = 0
            (s2x - s2y - r2 + 1)
        ]
        s2_neg_bounds = [
            # y = -x - r  (add x and r to both sides)
            # y + x + r = 0
            (s2x + s2y + r2 + 1),
            # y = -x + r  (add x and subtract r from both sides)
            # y + x - r = 0
            (s2x + s2y - r2 + 1)
        ]

        # for each combination of perpendicular boundaries (s1_pos is perpendicular to s2_neg) for these two sensors:
        #  - get the intersection point
        #  - check if the point is within the limit
        #  - check that the point is further away from every sensor's closest beacon
        #  - return the value if the above are true
        for pos, neg in product(s1_pos_bounds, s2_neg_bounds):
            # get the intersect point, still not quite sure why this works exactly
            x = (pos + neg) // 2
            y = pos - x
            if 0 <= x <= maxv and 0 <= y <= maxv:
                if all(dist(s, (x, y)) > radii[s] for s in radii):
                    return x * 4_000_000 + y

        for pos, neg in product(s1_neg_bounds, s2_pos_bounds):
            x = (pos + neg) // 2
            y = pos - x
            if 0 <= x <= maxv and 0 <= y <= maxv:
                if all(dist(s, (x, y)) > radii[s] for s in radii):
                    return x * 4_000_000 + y


# part 1 solution is really slow
# print(scan_y(test_inputs, 10))
# print()
# print(scan_y(inputs, 2000000))
# print()

start = time.time()
print(find_beacon(test_inputs, 20))
print(f"{time.time() - start}")
print()

start = time.time()
print(find_beacon(inputs, 4_000_000))
print(f"{time.time() - start}")
