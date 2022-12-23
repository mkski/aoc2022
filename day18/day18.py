inputs = [tuple(map(int, l.split(","))) for l in open("in").read().split("\n")]
test = [tuple(map(int, l.split(","))) for l in open("in-test").read().split("\n")]


def touching(c1, c2):
    return (
        (abs(c1[0] - c2[0]) == 1 and c1[1] == c2[1] and c1[2] == c2[2]) or
        (abs(c1[1] - c2[1]) == 1 and c1[0] == c2[0] and c1[2] == c2[2]) or
        (abs(c1[2] - c2[2]) == 1 and c1[0] == c2[0] and c1[1] == c2[1])
    )


def surface_area(inputs):
    area = 0
    xmin, xmax = ymin, ymax = zmin, zmax = 999, 0
    for c1 in inputs:
        n_touching = 0
        xmin, xmax = min([xmin, c1[0]]), max([xmax, c1[0]])
        ymin, ymax = min([ymin, c1[1]]), max([ymax, c1[1]])
        zmin, zmax = min([zmin, c1[2]]), max([zmax, c1[2]])
        for c2 in inputs:
            if touching(c1, c2):
                n_touching += 1
        area += 6 - n_touching
    return area, xmin, xmax, ymin, ymax, zmin, zmax


def external_area(inputs, xmin, xmax, ymin, ymax, zmin, zmax):
    to_check = [(xmin-1, ymin-1, zmin-1)]
    checked = set()
    area = 0
    while to_check:
        pos = to_check.pop(0)
        checked.add(pos)
        x, y, z = pos
       
        neighbors = [
            (x+1, y, z),
            (x-1, y, z),
            (x, y+1, z),
            (x, y-1, z),
            (x, y, z+1),
            (x, y, z-1)
        ]

        for neighbor in neighbors:
            if (
                xmin-1 <= neighbor[0] <= xmax+1 and
                ymin-1 <= neighbor[1] <= ymax+1 and
                zmin-1 <= neighbor[2] <= zmax+1 and
                neighbor not in checked and
                neighbor not in to_check
            ):
                if neighbor in inputs:
                    area += 1
                else:
                    to_check.append(neighbor)
    return area


area, *minmax = surface_area(inputs)
print(area)
# print(*minmax)
air_bubbles = external_area(inputs, *minmax)
# air_area, *_ = surface_area(air_bubbles)
print(air_bubbles)
